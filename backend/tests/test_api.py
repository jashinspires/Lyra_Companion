"""Integration tests for Lyra backend API."""

from __future__ import annotations

import pytest


@pytest.mark.anyio("asyncio")
async def test_health_check(client) -> None:
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio("asyncio")
async def test_chat_session_returns_reply(client) -> None:
    payload = {
        "messages": [
            {"role": "user", "content": "I'm feeling anxious about tomorrow."}
        ]
    }
    response = await client.post("/api/chat/session", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["reply"]["content"]
    assert body["safety"] is not None
    assert body["safety"]["crisis_detected"] is False
    assert isinstance(body.get("suggestions"), list)


@pytest.mark.anyio("asyncio")
async def test_journal_flow(client) -> None:
    payload = {
        "title": "Evening reflection",
        "content": "Today felt heavy but I made it through.",
        "mood": "sad",
        "tags": ["daily"],
    }
    create_response = await client.post("/api/journal/user-1/entries", json=payload)
    assert create_response.status_code == 201

    list_response = await client.get("/api/journal/user-1/entries")
    entries = list_response.json()
    assert list_response.status_code == 200
    assert len(entries) == 1
    assert entries[0]["title"] == "Evening reflection"

    summary_response = await client.get("/api/journal/user-1/summary")
    summary = summary_response.json()
    assert summary_response.status_code == 200
    assert summary["total_entries"] == 1
    assert summary["mood_counts"]["sad"] == 1


@pytest.mark.anyio("asyncio")
async def test_mood_logging_and_trend(client) -> None:
    await client.post(
        "/api/mood/user-2/logs",
        json={"mood": "anxious", "intensity": 4, "notes": "upcoming presentation"},
    )
    await client.post(
        "/api/mood/user-2/logs",
        json={"mood": "calm", "intensity": 2, "notes": "after breathing exercise"},
    )

    logs_response = await client.get("/api/mood/user-2/logs")
    assert logs_response.status_code == 200
    logs = logs_response.json()
    assert len(logs) == 2

    trend_response = await client.get("/api/mood/user-2/trend")
    assert trend_response.status_code == 200
    trend = trend_response.json()
    assert len(trend) == 1
    assert "average_intensity" in trend[0]


@pytest.mark.anyio("asyncio")
async def test_safety_check_detects_crisis(client) -> None:
    payload = {
        "text": "Sometimes I feel like I want to end it all.",
        "locale": "en-US",
    }
    response = await client.post("/api/safety/check", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["crisis_detected"] is True
    assert body["risk_level"] == "high"
    assert body["hotline"]
