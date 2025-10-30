from fastapi import FastAPI

from app.core.config import get_settings
from app.api.v1.routes import health

settings = get_settings()


def create_app() -> FastAPI:
	"""Create and configure the FastAPI application."""
	app = FastAPI(title=settings.app_name)

	# Register versioned API router
	app.include_router(health.router, prefix="/api/v1")

	# simple root health check
	@app.get("/", tags=["root"])
	async def root():
		return {"message": f"{settings.app_name} is running"}

	return app


app = create_app()
