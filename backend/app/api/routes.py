from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.db.session import database_is_reachable

router = APIRouter()


@router.get("/health", tags=["system"])
def health() -> dict[str, str | bool]:
    settings = get_settings()
    return {"status": "ok", "service": settings.app_name, "environment": settings.app_env, "database": database_is_reachable()}


@router.get("/health/ready", tags=["system"])
def readiness() -> dict[str, str | bool]:
    if not database_is_reachable():
        raise HTTPException(status_code=503, detail="Database is not ready")
    return {"status": "ready", "database": True}

