from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import oauth2, schemas
from app.database import get_db
from app.models import Post, User, Vote

router = APIRouter(
    prefix = "/votes",
    tags = ["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(payload: schemas.Vote,
         db: Session = Depends(get_db),
         current_user: User = Depends(oauth2.get_current_user)):
    
    vote = db.query(Vote) \
            .filter(Vote.post_id == payload.post_id, 
                    Vote.user_id == current_user.id) \
            .first()
    
    if vote:
        db.delete(vote)
        db.commit()
    else:
        found_post = db.query(Post).filter(Post.id==payload.post_id).first()
        if found_post:
            vote = Vote(post_id=payload.post_id, user_id=current_user.id)
            db.add(vote)
            db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {payload.post_id} not found")
