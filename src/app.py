from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.config import settings
from src.core.register import register_core


def create_app() -> FastAPI:
    app = FastAPI(
        title="knowledge_extraction_service",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.ENVIRONMENT == "development" else None,
    )

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,  # must be set in your config
        same_site="lax",                 # optional, helps with cookies
        session_cookie="knowledge_session"  # optional: custom cookie name
    )

    register_core(app)
    return app


app = create_app()
