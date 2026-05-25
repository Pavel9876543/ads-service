from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/advertisement", response_model=schemas.AdOut)
def create(ad: schemas.AdCreate, db: Session = Depends(get_db)):
    return crud.create_ad(db, ad)


@app.get("/advertisement/{ad_id}", response_model=schemas.AdOut)
def get(ad_id: int, db: Session = Depends(get_db)):
    ad = crud.get_ad(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Not found")
    return ad


@app.patch("/advertisement/{ad_id}", response_model=schemas.AdOut)
def update(ad_id: int, ad: schemas.AdUpdate, db: Session = Depends(get_db)):
    updated = crud.update_ad(db, ad_id, ad)
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    return updated


@app.delete("/advertisement/{ad_id}")
def delete(ad_id: int, db: Session = Depends(get_db)):
    ad = crud.delete_ad(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}


@app.get("/advertisement")
def search(title: str | None = None, author: str | None = None,
            min_price: float | None = None, max_price: float | None = None,
            db: Session = Depends(get_db)):

    filters = {k: v for k, v in {
        "title": title,
        "author": author,
        "min_price": min_price,
        "max_price": max_price
    }.items() if v is not None}

    return crud.search_ads(db, filters)