from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from backend.api.routes import router
from backend.core.config import settings
from backend.database.session import engine
from redis.asyncio import Redis

app = FastAPI(title="VideoForge API", version="4.2.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api/v1")

@app.get("/api/v1/health")
async def health():
    return {"status": "ok", "service": "videoforge-api", "version": "4.2.0"}

@app.get("/api/v1/ready")
async def ready():
    checks = {"database": False, "redis": False}
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception:
        pass
    redis = Redis.from_url(settings.redis_url)
    try:
        checks["redis"] = bool(await redis.ping())
    except Exception:
        pass
    finally:
        await redis.aclose()
    status = "ready" if all(checks.values()) else "not_ready"
    return {"status": status, "checks": checks}
