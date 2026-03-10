from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router
from app.db.postgres import engine
from app.db.models import Base
from app.cache.redis import redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Establishing Redis & DB connection")
    
    # DB setup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Redis check
    await redis_client.ping()
    print("Redis connected")

    yield

    print("Shutting down service")
    await redis_client.close()

app = FastAPI(
    title="Distributed Document Search Service",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)
    
@app.get("/health")
async def health():
    try:
        await redis_client.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "down"

    try:
        async with engine.begin():
            db_status = "ok"
    except Exception:
        db_status = "down"

    return {
        "status": "healthy",
        "services": {
            "postgres": db_status,
            "redis": redis_status
        }
    }