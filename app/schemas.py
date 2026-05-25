from pydantic import BaseModel
from datetime import datetime

class AdBase(BaseModel):
    title: str
    description: str
    price: float
    author: str

class AdCreate(AdBase):
    pass

class AdUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None

class AdOut(AdBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True