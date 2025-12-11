from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..core.config import get_settings
from ..db.database import initialize_database
from .notes_router import router as notes_router

settings = get_settings()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    openapi_tags=[
        {"name": "Notes", "description": "Operations on personal notes"},
        {"name": "Health", "description": "Health and system status"},
    ],
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database and create tables if needed."""
    initialize_database()


@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Basic health check endpoint to verify the service is running.",
)
def health_check():
    """Return service health."""
    return {"message": "Healthy"}


# Mount API routers under /api/v1
app.include_router(notes_router, prefix=f"{settings.api_prefix}")
