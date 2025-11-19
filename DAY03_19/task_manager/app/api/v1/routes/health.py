from fastapi import APIRouter

from app.api.v1.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health():
    """Simple health check endpoint."""
    return {"status": "ok"}
