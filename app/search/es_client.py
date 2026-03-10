from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch(
    hosts=["http://elasticsearch:9200"]
)