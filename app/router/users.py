from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import utils
from ..models import User
from ..schemas import UserCreate, UserResponse
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, 
                db: Session = Depends(get_db)) -> UserResponse:
    new_user = User(
        email=payload.email, 
        hashed_password=utils.hash(payload.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)) -> UserResponse:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")
    return user