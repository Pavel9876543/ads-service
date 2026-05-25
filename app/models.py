from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="user",
        nullable=False
    )

    advertisements = relationship(
        "Advertisement",
        back_populates="owner"
    )


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)
    description = Column(String)

    price = Column(Float)

    # оставляем для совместимости/поиска
    author = Column(String, index=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="advertisements"
    )