# app/schemas.py

from datetime import datetime
from pydantic import BaseModel, Field


class AdBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200
    )

    description: str = Field(
        min_length=1,
        max_length=1000
    )

    price: float = Field(
        gt=0
    )

    author: str = Field(
        min_length=1,
        max_length=100
    )


class AdCreate(AdBase):
    pass


class AdUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=1000
    )

    price: float | None = Field(
        default=None,
        gt=0
    )

    author: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )


class AdOut(AdBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }