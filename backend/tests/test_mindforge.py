"""
MINDFORGE — Pytest Test Stubs
Run: pytest backend/tests/ -v
"""
import pytest


# ─── Health ───────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_endpoint():
    from httpx import AsyncClient, ASGITransport
    from main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ─── Tasks ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_and_get_task():
    from httpx import AsyncClient, ASGITransport
    from main import app

    payload = {
        "title": "Test Assignment",
        "instructions": "Answer all questions",
        "target_url": "http://example.com/assignment",
        "priority": "normal",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        post_resp = await client.post("/api/tasks/", json=payload)
        assert post_resp.status_code == 201
        task_id = post_resp.json()["id"]

        get_resp = await client.get(f"/api/tasks/{task_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == "Test Assignment"


# ─── Voice Intent Parsing ─────────────────────────────────────────────────────

def test_intent_parse_fallback():
    """Intent parser should return raw command on failure."""
    from agents.voice_agent import VoiceAgent
    import asyncio

    agent = VoiceAgent()
    # Monkey-patch gemini to raise exception
    agent.gemini.answer_question = lambda _: "not valid json {{{"
    result = agent.parse_intent("go to google and search python")
    assert result["action"] == "unknown"
    assert result["target"] == "go to google and search python"


# ─── Utils ────────────────────────────────────────────────────────────────────

def test_truncate():
    from utils.helpers import truncate
    assert truncate("hello", 3) == "hel..."
    assert truncate("hello", 10) == "hello"


def test_is_valid_url():
    from utils.helpers import is_valid_url
    assert is_valid_url("https://google.com") is True
    assert is_valid_url("not-a-url") is False
