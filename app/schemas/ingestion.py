from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IngestionBase(BaseModel):
    document_id: int
    status: str

class IngestionCreate(IngestionBase):
    pass

class IngestionUpdate(BaseModel):
    status: Optional[str] = None

class IngestionOut(IngestionBase):
    id: int
    started_at: Optional[datetime]

    class Config:
        from_attributes  = True
