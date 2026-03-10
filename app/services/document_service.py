from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.db.models import Document
from app.search.indexer import index_document


class DocumentService:

    async def create_document(self, db, tenant_id, data):
        document = Document(
            tenant_id=tenant_id,
            title=data.title,
            content=data.content
        )

        db.add(document)
        
        await db.commit()
        await db.refresh(document)

        await index_document(document)

        return document


    async def get_document(self, db, tenant_id, doc_id):
        result = await db.execute(
            select(Document).where(
                Document.tenant_id == tenant_id,
                Document.id == doc_id
            )
        )

        return result.scalar_one_or_none()


    async def delete_document(self, db, tenant_id, doc_id):
        result = await db.execute(
            select(Document).where(
                Document.tenant_id == tenant_id,
                Document.id == doc_id
            )
        )

        document = result.scalar_one_or_none()

        if not document:
            return None

        await db.delete(document)
        await db.commit()

        return document