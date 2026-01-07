from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import get_db
from app.exceptions import CustomException
from app.models.models import User
from app.schemas.schemas import UserCreate
from app.services.password_hash import hash_password


def create_user(user: UserCreate, db: Session = Depends(get_db)):
    stmt = select(User).where(User.phone_number == user.phone_number)
    db_user = db.execute(stmt).scalar_one_or_none()
    if db_user:
        raise CustomException(status_code=400, detail="User already exists")

    user.password = hash_password(user.password)
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}
