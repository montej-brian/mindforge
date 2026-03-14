"""
MINDFORGE — Tasks API Routes
CRUD for the assignment task queue.
"""
import logging
from typing import List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime

from fastapi import APIRouter, HTTPException

from models.schemas import Task, TaskCreate, TaskStatus, Priority

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory store (replace with SQLAlchemy DB in production)
_task_store: Dict[str, Task] = {}


@router.post("/", response_model=Task, status_code=201)
async def create_task(payload: TaskCreate):
    """Create a new assignment task in the queue."""
    task = Task(
        id=uuid4(),
        **payload.model_dump(),
        status=TaskStatus.PENDING,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    _task_store[str(task.id)] = task
    logger.info(f"Task created: {task.id} — {task.title}")
    return task


@router.get("/", response_model=List[Task])
async def list_tasks(status: TaskStatus | None = None, priority: Priority | None = None):
    """List all tasks, optionally filtered by status or priority."""
    tasks = list(_task_store.values())
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    return sorted(tasks, key=lambda t: t.created_at, reverse=True)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: UUID):
    task = _task_store.get(str(task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=Task)
async def update_task(task_id: UUID, updates: Dict[str, Any]):
    task = _task_store.get(str(task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = task.model_copy(update={**updates, "updated_at": datetime.utcnow()})
    _task_store[str(task_id)] = updated
    return updated


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID):
    if str(task_id) not in _task_store:
        raise HTTPException(status_code=404, detail="Task not found")
    del _task_store[str(task_id)]
