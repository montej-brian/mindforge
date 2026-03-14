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

from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.schemas import (
    AgentRunRequest, AgentRunResponse,
    AgentStatusResponse, TaskStatus,
)
from models.database_models import TaskDB
from agents.orchestrator import run_task
from database import get_db, AsyncSessionLocal

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(request: AgentRunRequest, background_tasks: BackgroundTasks):
    """Spawn an orchestrator run for the given command. Returns a task_id."""
    task_id = request.task_id or uuid4()
    
    # Ensure task exists in DB or create a placeholder
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(TaskDB).where(TaskDB.id == str(task_id)))
        db_task = result.scalar_one_or_none()
        
        if not db_task:
            db_task = TaskDB(
                id=str(task_id),
                title=f"Agent Run: {request.command[:50]}...",
                instructions=request.command,
                status=TaskStatus.PENDING
            )
            db.add(db_task)
            await db.commit()
            await db.refresh(db_task)

    async def _run_task_bg(tid: str, cmd: str, ctx: Optional[Dict[str, Any]]):
        async with AsyncSessionLocal() as db:
            # Mark running
            result = await db.execute(select(TaskDB).where(TaskDB.id == tid))
            task = result.scalar_one_or_none()
            if task:
                task.status = TaskStatus.RUNNING
                await db.commit()

            # Run orchestrator
            res = await run_task(cmd, context=ctx)
            
            # Update final status
            result = await db.execute(select(TaskDB).where(TaskDB.id == tid))
            task = result.scalar_one_or_none()
            if task:
                if res["success"]:
                    task.status = TaskStatus.COMPLETED
                    task.result = res["output"]
                else:
                    task.status = TaskStatus.FAILED
                    task.error = res["output"]
                task.updated_at = datetime.utcnow()
                await db.commit()

    background_tasks.add_task(_run_task_bg, str(task_id), request.command, request.context)
    
    return AgentRunResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        message="Task initialized and queued in background",
    )


@router.get("/status/{task_id}", response_model=AgentStatusResponse)
async def get_task_status(task_id: str, db: AsyncSession = Depends(get_db)):
    """Get the current status of an agent task from DB."""
    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return AgentStatusResponse(
        task_id=task.id,
        status=task.status,
        output=task.result,
        error=task.error,
        # Steps are currently not persisted in TaskDB, using empty list or could be added later
        steps=[] 
    )


@router.get("/tasks")
async def list_agent_tasks(db: AsyncSession = Depends(get_db)):
    """Return all agent tasks from DB."""
    result = await db.execute(select(TaskDB).order_by(TaskDB.created_at.desc()))
    return result.scalars().all()


@router.delete("/tasks/{task_id}")
async def delete_agent_task(task_id: str, db: AsyncSession = Depends(get_db)):
    """Remove a task record from DB."""
    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(task)
    await db.commit()
    return {"message": "Task removed"}
