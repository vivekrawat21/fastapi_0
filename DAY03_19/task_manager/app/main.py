from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.core.models import Base
from app.api.v1.routes import health, tasks
from app.middleware.exception_middleware import exception_middleware_factory


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.frontend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(exception_middleware_factory())

    app.include_router(health.router, prefix="/api/v1")
    app.include_router(tasks.router, prefix="/api/v1")


 
    @app.get("/", tags=["root"])
    async def root():
        return {"message": f"{settings.app_name} is running"}

    return app


app = create_app()
