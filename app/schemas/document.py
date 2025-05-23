from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentOut(DocumentBase):
    id: int
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes  = True

class DocumentUpdate(BaseModel):
    title: str
    content: str
