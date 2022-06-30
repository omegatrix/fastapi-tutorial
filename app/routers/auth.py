from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import Token
from ..models import User
from ..utils import verify_password
from ..oauth2 import generate_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/authenticate", response_model=Token)
def authenticate(
    credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == credentials.username).first()

    if user and verify_password(credentials.password, user.password):
        access_token = generate_access_token(data={"user_id": user.id})

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
