import json

from app.cache.redis import redis_client


class CacheService:
    async def get(self, key: str):
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(self, key: str, value, ttl: int = 60):
        await redis_client.set(key, json.dumps(value), ex=ttl)