import re
from fastapi import Depends
from sqlalchemy.orm import Session
from app.enum import UserType
from app.schemas.schemas import UserCreate, Login, LoginResponse
from app.db import get_db
from app.exceptions import CustomException
from app.services.password_hash import hash_password, verify_password
from app.services.token import create_access_token
from app.models.models import User


def login(user: Login, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.phone_number == user.phone_number).first()

    if not db_user:
        return CustomException(
            status_code=422, data={"phone_number": "User does not exist"}
        )

    if not db_user.is_active:
        return CustomException(
            status_code=422, data={"phone_number": "User is not active"}
        )

    if not verify_password(user.password, db_user.password):
        return CustomException(status_code=422, data={"password": "Invalid password"})

    response_user = LoginResponse.model_validate(db_user)
    token = create_access_token(
        {"sub": str(db_user.id), "phone_number": db_user.phone_number}
    )
    response_user.access_token = token

    return response_user


def register(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.phone_number == user.phone_number).first()

    if db_user:
        raise CustomException(
            status_code=422, data={"phone_number": "User already exists"}
        )

    user.password = hash_password(user.password)

    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    response_user = LoginResponse.model_validate(db_user)
    token = create_access_token(
        {"sub": str(db_user.id), "phone_number": db_user.phone_number}
    )
    response_user.access_token = token
    return response_user
