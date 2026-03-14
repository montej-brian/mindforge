"""
MINDFORGE — Pydantic Models
Shared data schemas for API requests, responses, and internal state.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# ─── Enums ────────────────────────────────────────────────────────────────────

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentType(str, Enum):
    ORCHESTRATOR = "orchestrator"
    BROWSER = "browser"
    VOICE = "voice"
    ASSIGNMENT = "assignment"


class Priority(str, Enum):
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


# ─── Voice Models ─────────────────────────────────────────────────────────────

class VoiceCommandRequest(BaseModel):
    """POST /api/voice/command — incoming voice command (text or audio ref)"""
    transcript: Optional[str] = None
    audio_url: Optional[str] = None
    language: str = "en"


class VoiceCommandResponse(BaseModel):
    transcript: str
    intent: Dict[str, Any]
    task_id: Optional[UUID] = None


# ─── Task Models ──────────────────────────────────────────────────────────────

class TaskCreate(BaseModel):
    """Create a new assignment task."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    target_url: Optional[str] = None
    instructions: str
    priority: Priority = Priority.NORMAL


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    target_url: Optional[str] = None
    instructions: str
    priority: Priority = Priority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    class Config:
        use_enum_values = True


# ─── Agent Models ─────────────────────────────────────────────────────────────

class AgentRunRequest(BaseModel):
    """POST /api/agents/run — kick off an agent task."""
    command: str = Field(..., min_length=1)
    task_id: Optional[UUID] = None
    context: Optional[Dict[str, Any]] = None


class AgentRunResponse(BaseModel):
    task_id: UUID
    status: TaskStatus
    message: str


class AgentStatusResponse(BaseModel):
    task_id: UUID
    status: TaskStatus
    output: Optional[str] = None
    steps: List[Dict[str, Any]] = []
    error: Optional[str] = None


# ─── WebSocket Event Models ────────────────────────────────────────────────────

class WSEventType(str, Enum):
    AGENT_STARTED = "agent_started"
    AGENT_STEP = "agent_step"
    AGENT_COMPLETED = "agent_completed"
    AGENT_ERROR = "agent_error"
    BROWSER_ACTION = "browser_action"
    VOICE_DETECTED = "voice_detected"
    STATUS_UPDATE = "status_update"


class WSEvent(BaseModel):
    event: WSEventType
    task_id: Optional[UUID] = None
    agent: Optional[AgentType] = None
    data: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
