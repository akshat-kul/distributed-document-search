from fastapi import HTTPException
from app.cache.redis import redis_client


async def rate_limit(tenant_id: int):

    key = f"rate:{tenant_id}"

    count = await redis_client.incr(key)

    if count == 1:
        await redis_client.expire(key, 60)

    if count > 100:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )