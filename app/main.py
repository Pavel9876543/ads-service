# app/main.py

from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models, schemas

# Создание таблиц
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Создание объявления
@app.post(
    "/advertisement",
    response_model=schemas.AdOut,
    status_code=status.HTTP_201_CREATED
)
def create_advertisement(
    ad: schemas.AdCreate,
    db: Session = Depends(get_db)
):
    db_ad = models.Advertisement(**ad.model_dump())

    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)

    return db_ad


# Получение объявления по ID
@app.get(
    "/advertisement/{ad_id}",
    response_model=schemas.AdOut
)
def get_advertisement(
    ad_id: int,
    db: Session = Depends(get_db)
):
    ad = db.query(models.Advertisement).filter(
        models.Advertisement.id == ad_id
    ).first()

    if ad is None:
        raise HTTPException(
            status_code=404,
            detail="Advertisement not found"
        )

    return ad


# Поиск объявлений
@app.get(
    "/advertisement",
    response_model=list[schemas.AdOut]
)
def search_advertisements(
    title: str | None = None,
    description: str | None = None,
    author: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    created_after: datetime | None = None,
    created_before: datetime | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Advertisement)

    # Поиск по title
    if title:
        query = query.filter(
            models.Advertisement.title.contains(title)
        )

    # Поиск по description
    if description:
        query = query.filter(
            models.Advertisement.description.contains(description)
        )

    # Поиск по author
    if author:
        query = query.filter(
            models.Advertisement.author.contains(author)
        )

    # Минимальная цена
    if min_price is not None:
        query = query.filter(
            models.Advertisement.price >= min_price
        )

    # Максимальная цена
    if max_price is not None:
        query = query.filter(
            models.Advertisement.price <= max_price
        )

    # Дата создания ОТ
    if created_after:
        query = query.filter(
            models.Advertisement.created_at >= created_after
        )

    # Дата создания ДО
    if created_before:
        query = query.filter(
            models.Advertisement.created_at <= created_before
        )

    return query.all()


# Обновление объявления
@app.patch(
    "/advertisement/{ad_id}",
    response_model=schemas.AdOut
)
def update_advertisement(
    ad_id: int,
    ad_update: schemas.AdUpdate,
    db: Session = Depends(get_db)
):
    db_ad = db.query(models.Advertisement).filter(
        models.Advertisement.id == ad_id
    ).first()

    if db_ad is None:
        raise HTTPException(
            status_code=404,
            detail="Advertisement not found"
        )

    update_data = ad_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_ad, field, value)

    db.commit()
    db.refresh(db_ad)

    return db_ad


# Удаление объявления
@app.delete(
    "/advertisement/{ad_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_advertisement(
    ad_id: int,
    db: Session = Depends(get_db)
):
    db_ad = db.query(models.Advertisement).filter(
        models.Advertisement.id == ad_id
    ).first()

    if db_ad is None:
        raise HTTPException(
            status_code=404,
            detail="Advertisement not found"
        )

    db.delete(db_ad)
    db.commit()

    return None