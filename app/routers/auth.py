from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..oauth2 import generate_access_token
from ..schemas import Token
from ..utils import verify_password

router = APIRouter(prefix="/authenticate", tags=["Authentication"])


@router.post("/", response_model=Token)
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
