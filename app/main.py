
from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.api.routes.documents import router as documents_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="An AI-powered study assistant with document-based question answering."
)


@app.get("/")
def home():
    """Welcome endpoint."""

    return {
        "message": "Welcome to AI Study Assistant!",
        "status": "Application is running"
    }


@app.get("/health")
def health_check():
    """Check application health."""

    return {
        "status": "healthy"
    }


# Register Chat API
app.include_router(
    chat_router,
    prefix="/api/v1",
    tags=["Chat"]
)
# Register Documents API
app.include_router(
    documents_router,
    prefix="/api/v1",
    tags=["Documents"]
)