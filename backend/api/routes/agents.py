"""
MINDFORGE — Agents API Routes
POST /api/agents/run    — kick off an agent task from a command string
GET  /api/agents/status — check status of a running task
GET  /api/agents/tasks  — list all tasks in memory
"""
import asyncio
import logging
from typing import Dict, Any
from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException

from models.schemas import (
    AgentRunRequest, AgentRunResponse,
    AgentStatusResponse, TaskStatus,
)
from agents.orchestrator import run_task

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory task store (replace with DB in production)
_tasks: Dict[str, Dict[str, Any]] = {}


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(request: AgentRunRequest, background_tasks: BackgroundTasks):
    """Spawn an orchestrator run for the given command. Returns a task_id."""
    task_id = uuid4()
    _tasks[str(task_id)] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "command": request.command,
        "output": None,
        "steps": [],
        "error": None,
    }

    async def _run():
        _tasks[str(task_id)]["status"] = TaskStatus.RUNNING
        result = await run_task(request.command, context=request.context)
        if result["success"]:
            _tasks[str(task_id)]["status"] = TaskStatus.COMPLETED
            _tasks[str(task_id)]["output"] = result["output"]
            _tasks[str(task_id)]["steps"] = result["steps"]
        else:
            _tasks[str(task_id)]["status"] = TaskStatus.FAILED
            _tasks[str(task_id)]["error"] = result["output"]

    background_tasks.add_task(_run)
    return AgentRunResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        message="Task queued successfully",
    )


@router.get("/status/{task_id}", response_model=AgentStatusResponse)
async def get_task_status(task_id: UUID):
    """Get the current status of an agent task."""
    record = _tasks.get(str(task_id))
    if not record:
        raise HTTPException(status_code=404, detail="Task not found")
    return AgentStatusResponse(**record)


@router.get("/tasks")
async def list_tasks():
    """Return all tasks (paginate in production)."""
    return list(_tasks.values())


@router.delete("/tasks/{task_id}")
async def cancel_task(task_id: UUID):
    """Remove a task record."""
    if str(task_id) not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del _tasks[str(task_id)]
    return {"message": "Task removed"}
