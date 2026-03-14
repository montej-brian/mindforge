"""
MINDFORGE — Tasks API Routes
CRUD for the assignment task queue.
"""
import logging
from typing import List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from models.schemas import Task, TaskCreate, TaskStatus, Priority
from models.database_models import TaskDB
from database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=Task, status_code=201)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    """Create a new assignment task in the database."""
    db_task = TaskDB(**payload.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    logger.info(f"Task created: {db_task.id} — {db_task.title}")
    return db_task


@router.get("/", response_model=List[Task])
async def list_tasks(
    status: TaskStatus | None = None, 
    priority: Priority | None = None,
    db: AsyncSession = Depends(get_db)
):
    """List all tasks, optionally filtered by status or priority."""
    query = select(TaskDB)
    if status:
        query = query.where(TaskDB.status == status)
    if priority:
        query = query.where(TaskDB.priority == priority)
    
    result = await db.execute(query.order_by(TaskDB.created_at.desc()))
    return result.scalars().all()


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=Task)
async def update_task(task_id: str, updates: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in updates.items():
        if hasattr(task, key):
            setattr(task, key, value)
    
    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(TaskDB).where(TaskDB.id == task_id))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.commit()
