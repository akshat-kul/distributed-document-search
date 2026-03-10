from app.cache.cache_service import CacheService
from app.search.es_client import es

INDEX_NAME = "documents"
cache = CacheService()

class SearchService:

    async def search(self, tenant_id: int, query: str):

        cache_key = f"search:{tenant_id}:{query}"

        cached = await cache.get(cache_key)
        if cached:
            print("CACHE HIT")
            return cached

        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title", "content"],
                                "fuzziness": "AUTO"
                            }
                        }
                    ],
                    "filter": [
                        {"term": {"tenant_id": tenant_id}}
                    ]
                }
            },
            "highlight": {
                "fields": {
                    "content": {},
                    "title": {}
                }
            }
        }

        response = await es.search(index=INDEX_NAME, body=body)

        hits = response["hits"]["hits"]

        results = []

        for hit in hits:
            doc = hit["_source"]
            doc["highlight"] = hit.get("highlight", {})
            results.append(doc)

        await cache.set(cache_key, results, ttl=60)

        return results