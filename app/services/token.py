import uuid
import jwt
from datetime import datetime, timedelta, timezone, time
from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_WEEKS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_WEEKS"))

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    data = {
        **data,
        "exp": (
            datetime.now(timezone.utc)
            + (expires_delta or timedelta(weeks=ACCESS_TOKEN_EXPIRE_WEEKS))
        ).timestamp(),
        "iat": datetime.now(timezone.utc),
    }
    print(data)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def validate_token(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(decoded_token["exp"])
        print(datetime.now(timezone.utc))
        return (
            decoded_token
            if decoded_token["exp"] >= datetime.now(timezone.utc).timestamp()
            else None
        )
    except jwt.PyJWTError:
        return {}


async def get_user_id_from_token(
    auth: HTTPAuthorizationCredentials = Depends(security),
):
    token = auth.credentials
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return uuid.UUID(decoded_token["sub"])
    except jwt.PyJWTError:
        return None
