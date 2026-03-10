from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch(
    hosts=["http://localhost:9200"]
)