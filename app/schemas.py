from datetime import datetime

from pydantic import BaseModel, Field


# =========================
# User schemas
# =========================

class UserCreate(BaseModel):
    username: str = Field(
        min_length=1,
        max_length=100
    )

    password: str = Field(
        min_length=4,
        max_length=100
    )


class UserUpdate(BaseModel):
    username: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    password: str | None = Field(
        default=None,
        min_length=4,
        max_length=100
    )


class UserOut(BaseModel):
    id: int
    username: str
    role: str

    model_config = {
        "from_attributes": True
    }


# =========================
# Auth schemas
# =========================

class LoginSchema(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    token: str


# =========================
# Advertisement schemas
# =========================

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
    owner_id: int | None = None

    model_config = {
        "from_attributes": True
    }