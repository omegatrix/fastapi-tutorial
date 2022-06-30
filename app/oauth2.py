from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .schemas import TokenData
from .database import get_db
from .models import User

SECRET_KEY = "fff4554cd2eaa467a3243a576b0c03ab3df82a5f968d83bd20f2873b76b0b572"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")


def generate_access_token(data: dict):
    to_encode = data.copy()
    to_expire = f"{datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}"

    to_encode.update({"expire": to_expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception: Exception) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
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
