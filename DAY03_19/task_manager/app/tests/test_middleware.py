import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_404_returns_problemdetails():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/non-existent-route")
        assert r.status_code == 404
        data = r.json()
        assert all(k in data for k in ("type", "title", "status", "detail", "instance", "timestamp", "trace_id"))
        assert data["status"] == 404


@pytest.mark.asyncio
async def test_cors_preflight_options():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        }
        r = await ac.options("/api/v1/tasks", headers=headers)
        assert r.status_code in (200, 204)
        assert r.headers.get("access-control-allow-origin") in ("http://localhost:5173", "*")
