from pydantic import BaseModel
from uuid import UUID


class DocumentCreate(BaseModel):
    title: str
    content: str


class DocumentResponse(BaseModel):
    id: UUID
    tenant_id: int
    title: str
    content: str

    class Config:
        from_attributes = True