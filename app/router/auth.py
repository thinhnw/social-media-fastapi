from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import utils, oauth2
from ..database import get_db
from ..schemas import Token, TokenData
from ..models import User

router = APIRouter(tags=["Auth"])

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
                db: Session = Depends(get_db)) -> Token:

    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return Token(access_token=access_token, token_type="bearer")