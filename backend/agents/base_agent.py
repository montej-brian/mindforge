import abc
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4

from models.protocol import (
    MACPMessage, AgentRole, AgentState, 
    MessagePriority, MessageType
)

logger = logging.getLogger(__name__)

class BaseAgent(abc.ABC):
    """
    Abstract Base Class for all MINDFORGE Agents.
    Enforces the MACP State Machine and communication patterns.
    """
    def __init__(self, role: AgentRole):
        self.role = role
        self.state = AgentState.IDLE
        self.current_task_id: Optional[str] = None
        self.logger = logging.getLogger(f"agent.{role.value}")

    def log_macp(self, level: int, msg_id: str, action: str):
        """Structured logging following M-LOG format."""
        ts = datetime.utcnow().isoformat()
        self.logger.log(
            level, 
            f"[{ts}] [{self.role.upper()}] [INFO] [{self.current_task_id}] [{msg_id}] [{self.state}] - ACTION: {action}"
        )

    async def transition_to(self, new_state: AgentState, msg_id: Optional[str] = None):
        """Handle state transitions with validation and logging."""
        old_state = self.state
        self.state = new_state
        self.log_macp(logging.INFO, msg_id or "INTERNAL", f"Transitioned from {old_state} to {new_state}")

    @abc.abstractmethod
    async def process_message(self, message: MACPMessage):
        """Standard entry point for all incoming MACP messages."""
        pass

    async def send_response(self, request: MACPMessage, payload: Dict[str, Any]):
        """Helper to send a response back to the original sender."""
        response = MACPMessage(
            parent_id=request.msg_id,
            sender=self.role,
            receiver=request.sender,
            type=MessageType.RESPONSE,
            payload=payload,
            priority=request.priority
        )
        # In a real implementation, this would call the Orchestrator/WS manager
        self.log_macp(logging.INFO, str(response.msg_id), f"Sent response to {request.sender}")
        return response

    async def handle_error(self, message: MACPMessage, error_msg: str):
        """Standard error reporting channel."""
        await self.transition_to(AgentState.ERROR, str(message.msg_id))
        error_resp = MACPMessage(
            parent_id=message.msg_id,
            sender=self.role,
            receiver=message.sender,
            type=MessageType.ERROR,
            payload={"error": error_msg, "code": 500},
            priority=MessagePriority.HIGH
        )
        self.log_macp(logging.ERROR, str(error_resp.msg_id), f"Reported error: {error_msg}")
        return error_resp
