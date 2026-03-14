from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

# ─── Intent Categories ────────────────────────────────────────────────────────

class CommandCategory(str, Enum):
    NAVIGATION = "navigation"
    CONTROL = "control"
    ACTION = "action"
    QUERY = "query"
    EMERGENCY = "emergency"

class NavigationIntent(str, Enum):
    GO_TO_URL = "go_to_url"
    HISTORY_BACK = "history_back"
    HISTORY_FORWARD = "history_forward"
    FOCUS_ELEMENT = "focus_element"

class ControlIntent(str, Enum):
    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    STOP = "stop"
    STATUS = "status"
    CONFIG = "config"

class ActionIntent(str, Enum):
    CLICK = "click"
    INPUT = "input"
    SUBMIT = "submit"
    UPLOAD = "upload"

class QueryIntent(str, Enum):
    QUESTION = "question"
    PROGRESS = "progress"
    HELP = "help"

class EmergencyIntent(str, Enum):
    PANIC = "panic"
    RESET = "reset"
    OVERRIDE = "override"

# ─── Intent Models ──────────────────────────────────────────────────────────

class VoiceIntent(BaseModel):
    """
    Structured representation of a parsed voice command.
    """
    category: CommandCategory
    intent: str  # One of the intent enums above
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 3  # Matches MACP MessagePriority (0-4)
    original_text: str
    requires_confirmation: bool = False
    confirmation_text: Optional[str] = None

class ParserResponse(BaseModel):
    """
    Final output from the NLP parser.
    """
    success: bool
    intent: Optional[VoiceIntent] = None
    error: Optional[str] = None
    suggested_response: str
