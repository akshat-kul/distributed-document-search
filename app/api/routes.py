from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.middleware.rate_limit import rate_limit
from app.schemas.document import DocumentCreate, DocumentResponse
from app.schemas.tenant import TenantCreate, TenantResponse
from app.services.tenant_service import TenantService
from app.services.document_service import DocumentService
from app.services.search_service import SearchService
from app.db.postgres import get_db


router = APIRouter()
document_service = DocumentService()
search_service = SearchService()
tenant_service = TenantService()

@router.post("/tenants", response_model=TenantResponse)
async def create_tenant(
    payload: TenantCreate,
    db: AsyncSession = Depends(get_db)
):

    tenant = await tenant_service.create_tenant(db, payload)

    return tenant

@router.post("/tenants/{tenant_id}/documents", response_model=DocumentResponse)
async def create_document(
    tenant_id: int,
    payload: DocumentCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        document = await document_service.create_document(db, tenant_id, payload)
        return document
    
    except Exception as e:
        print(f"Exception Occurred: {e}")
        raise


@router.get("/tenants/{tenant_id}/search")
async def search_documents(
    tenant_id: int,
    q: str
):
    try:
        await rate_limit(tenant_id)
        results = await search_service.search(tenant_id, q)
        return results
    
    except Exception as e:
        print(f"Exception Occurred: {e}")
        return []

@router.get("/tenants/{tenant_id}/documents/{doc_id}", response_model=DocumentResponse)
async def get_document(
    tenant_id: int,
    doc_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    try:
        document = await document_service.get_document(db, tenant_id, doc_id)

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return document

    except Exception as e:
        print(f"Exception Occurred: {e}")
        raise


@router.delete("/tenants/{tenant_id}/documents/{doc_id}")
async def delete_document(
    tenant_id: int,
    doc_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    try:
        document = await document_service.delete_document(db, tenant_id, doc_id)

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        return {"status": "deleted"}

    except Exception as e:
        print(f"Exception Occurred: {e}")
        raise