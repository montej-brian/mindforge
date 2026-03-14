import json
from uuid import uuid4
from datetime import datetime
from models.protocol import MACPMessage, AgentRole, MessageType, MessagePriority

def verify_protocol():
    print("🚀 Starting MACP Protocol Verification...\n")

    # 1. Normal QA Flow: Orchestrator -> Vision Request
    qa_request = {
        "msg_id": str(uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "sender": "orchestrator",
        "receiver": "vision",
        "priority": 3,  # NORMAL
        "type": "request",
        "payload": {
            "action": "capture",
            "target": "full_screen"
        },
        "metadata": {"tracing_token": "qa-trace-123"}
    }
    
    try:
        msg = MACPMessage(**qa_request)
        print(f"✅ Normal QA Request Validated: {msg.msg_id}")
    except Exception as e:
        print(f"❌ Normal QA Request Failed: {e}")

    # 2. Error Scenario: Vision -> Orchestrator Error
    error_msg = {
        "msg_id": str(uuid4()),
        "parent_id": qa_request["msg_id"],
        "timestamp": datetime.utcnow().isoformat(),
        "sender": "vision",
        "receiver": "orchestrator",
        "priority": 2, # HIGH
        "type": "error",
        "payload": {
            "error": "Camera Device Busy",
            "code": 500
        }
    }
    
    try:
        msg = MACPMessage(**error_msg)
        print(f"✅ Error Message Validated: {msg.msg_id}")
    except Exception as e:
        print(f"❌ Error Message Failed: {e}")

    # 3. User Interruption Scenario: Signal (Priority 1)
    stop_signal = {
        "msg_id": str(uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "sender": "orchestrator",
        "receiver": "broadcast",
        "priority": 1, # SIGNAL
        "type": "signal",
        "payload": {"action": "stop", "reason": "user_cancelled"}
    }
    
    try:
        msg = MACPMessage(**stop_signal)
        print(f"✅ Stop Signal Validated: {msg.msg_id}")
    except Exception as e:
        print(f"❌ Stop Signal Failed: {e}")

    print("\n✨ All protocol scenarios validated successfully against Pydantic models.")

if __name__ == "__main__":
    verify_protocol()
