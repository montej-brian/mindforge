from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

# ─── MACP Enums ───────────────────────────────────────────────────────────────

class AgentRole(str, Enum):
    ORCHESTRATOR = "orchestrator"
    VISION = "vision"
    COGNITION = "cognition"
    ACTION = "action"
    BROADCAST = "broadcast"

class MessageType(str, Enum):
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    SIGNAL = "signal"
    ERROR = "error"

class MessagePriority(IntEnum):
    EMERGENCY = 0
    SIGNAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4

class AgentState(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    WAITING = "waiting"
    ERROR = "error"
    SUSPENDED = "suspended"

# ─── MACP Core Models ─────────────────────────────────────────────────────────

class MACPMetadata(BaseModel):
    timeout_ms: int = 30000
    retries: int = 0
    tracing_token: Optional[str] = None

class MACPMessage(BaseModel):
    """
    Universal Message Envelope for MINDFORGE Agent Communication Protocol (MACP).
    Ref: protocol_specification.md
    """
    msg_id: UUID = Field(default_factory=uuid4)
    parent_id: Optional[UUID] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sender: AgentRole
    receiver: AgentRole
    priority: MessagePriority = MessagePriority.NORMAL
    type: MessageType
    payload: Dict[str, Any]
    metadata: MACPMetadata = Field(default_factory=MACPMetadata)

    class Config:
        use_enum_values = True

# ─── Scenario Examples (Type Hinting) ────────────────────────────────────────

class VisionCaptureRequest(BaseModel):
    action: str = "capture"
    target: str = "full_screen"
    ocr_enabled: bool = True

class ActionCommandRequest(BaseModel):
    command: str
    coordinates: Optional[Dict[str, int]] = None
    text: Optional[str] = None
