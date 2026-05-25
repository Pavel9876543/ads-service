from sqlalchemy.orm import Session
from . import models, schemas


def create_ad(db: Session, ad: schemas.AdCreate):
    db_ad = models.Advertisement(**ad.model_dump())
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad


def get_ad(db: Session, ad_id: int):
    return db.query(models.Advertisement).filter(models.Advertisement.id == ad_id).first()


def delete_ad(db: Session, ad_id: int):
    ad = get_ad(db, ad_id)
    if ad:
        db.delete(ad)
        db.commit()
    return ad


def update_ad(db: Session, ad_id: int, ad_update: schemas.AdUpdate):
    ad = get_ad(db, ad_id)
    if not ad:
        return None

    for key, value in ad_update.model_dump(exclude_unset=True).items():
        setattr(ad, key, value)

    db.commit()
    db.refresh(ad)
    return ad


def search_ads(db: Session, filters: dict):
    query = db.query(models.Advertisement)

    if "title" in filters:
        query = query.filter(models.Advertisement.title.contains(filters["title"]))
    if "author" in filters:
        query = query.filter(models.Advertisement.author.contains(filters["author"]))
    if "min_price" in filters:
        query = query.filter(models.Advertisement.price >= filters["min_price"])
    if "max_price" in filters:
        query = query.filter(models.Advertisement.price <= filters["max_price"])

    return query.all()