from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .schemas import TokenData
from .settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")


def generate_access_token(data: dict):
    to_encode = data.copy()
    to_expire = f"{datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expiry_minutes)}"

    to_encode.update({"expire": to_expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exception: Exception) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithm=settings.jwt_algorithm
        )
        user_id: str = payload.get("user_id")

        if not user_id:
            raise credentials_exception

        return TokenData(id=user_id)
    except JWTError:
        raise credentials_exception


def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token: TokenData = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()

    return user
