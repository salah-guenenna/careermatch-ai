from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.routes import router
from app.api.auth import router as auth_router, users_router
from app.api.resources import router as resources_router
from app.api.analyses import router as analyses_router
from app.api.dashboard import router as dashboard_router
from app.core.config import get_settings
from app.db.session import create_tables

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", description="CareerMatch AI REST API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "api", "*"])


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    return response
app.include_router(router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(resources_router)
app.include_router(analyses_router)
app.include_router(dashboard_router)


@app.on_event("startup")
def startup() -> None:
    create_tables()

