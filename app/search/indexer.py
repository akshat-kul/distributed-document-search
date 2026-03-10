from app.search.es_client import es

INDEX_NAME = "documents"


async def index_document(doc):
    await es.index(
        index=INDEX_NAME,
        id=str(doc.id),
        document={
            "tenant_id": doc.tenant_id,
            "title": doc.title,
            "content": doc.content
        }
    )