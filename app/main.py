from datetime import datetime

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from .database import engine, get_db

from . import models, schemas

from .auth import (
    hash_password,
    verify_password,
    create_token
)

from .security import get_current_user


# Создание таблиц
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# =========================
# Advertisement routes
# =========================

# Создание объявления
@app.post(
    "/advertisement",
    response_model=schemas.AdOut,
    status_code=status.HTTP_201_CREATED
)
def create_advertisement(
    ad: schemas.AdCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_ad = models.Advertisement(
        **ad.model_dump(),
        owner_id=current_user.id
    )

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
    current_user=Depends(get_current_user),
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

    # Проверка прав
    if (
        current_user.role != "admin"
        and db_ad.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    update_data = ad_update.model_dump(
        exclude_unset=True
    )

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
    current_user=Depends(get_current_user),
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

    # Проверка прав
    if (
        current_user.role != "admin"
        and db_ad.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    db.delete(db_ad)
    db.commit()

    return None

# =========================
# Auth routes
# =========================

# Логин
@app.post(
    "/login",
    response_model=schemas.TokenOut
)
def login(
    data: schemas.LoginSchema,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.username == data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_token({
        "user_id": user.id,
        "role": user.role
    })

    return {
        "token": token
    }


# =========================
# User routes
# =========================

# Создание пользователя
@app.post(
    "/user",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    db_user = models.User(
        username=user.username,
        password=hash_password(user.password),
        role="user"
    )

    db.add(db_user)

    db.commit()
    db.refresh(db_user)

    return db_user


# Получение пользователя
@app.get(
    "/user/{user_id}",
    response_model=schemas.UserOut
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# Обновление пользователя
@app.patch(
    "/user/{user_id}",
    response_model=schemas.UserOut
)
def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Проверка прав
    if (
        current_user.role != "admin"
        and current_user.id != user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    # Хеширование нового пароля
    if "password" in update_data:
        update_data["password"] = hash_password(
            update_data["password"]
        )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


# Удаление пользователя
@app.delete(
    "/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Проверка прав
    if (
        current_user.role != "admin"
        and current_user.id != user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    db.delete(user)
    db.commit()

    return None