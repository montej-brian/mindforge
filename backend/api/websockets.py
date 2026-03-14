"""
MINDFORGE — WebSocket Event Handler
Endpoint: ws://localhost:8000/ws/events
Broadcasts real-time agent progress events to all connected frontend clients.
"""
import asyncio
import json
import logging
from typing import Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from models.schemas import WSEvent
from models.protocol import MACPMessage

router = APIRouter()
logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages active WebSocket connections and broadcasts events."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WS client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"WS client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, event: WSEvent):
        """Send an event to all connected clients."""
        payload = event.model_dump_json()
        dead = set()
        for ws in self.active_connections:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.active_connections.discard(ws)

    async def send_to(self, websocket: WebSocket, event: WSEvent):
        """Send an event to a specific client."""
        await websocket.send_text(event.model_dump_json())

    async def broadcast_macp(self, message: MACPMessage):
        """Send a protocol-compliant message to all connected clients."""
        payload = message.model_dump_json()
        dead = set()
        for ws in self.active_connections:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.active_connections.discard(ws)


# Shared manager instance — importable by agents for broadcasting
manager = ConnectionManager()


@router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send connection confirmation
        await websocket.send_json({
            "event": "connected",
            "data": {"message": "MINDFORGE WebSocket connected"},
        })

        # Keep alive — listen for client messages (ping/pong or commands)
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                logger.debug(f"WS received: {msg}")
                # Echo back for now; extend to handle client-side commands
                await websocket.send_json({"event": "ack", "data": msg})
            except json.JSONDecodeError:
                await websocket.send_json({"event": "error", "data": {"message": "Invalid JSON"}})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
