from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import oauth2
from ..models import Post, User, Vote
from ..schemas import PostResponse, PostBase, PostWithVotesResponse
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
def get_posts(limit: int = 5,
              skip: int = 0,
              search: str = "",
              db: Session = Depends(get_db)) -> list[PostWithVotesResponse]:

    print(search + ".") 
    
    posts = db.query(Post, func.count(Vote.post_id).label("votes")) \
            .join(Vote, Vote.post_id == Post.id, isouter=True) \
            .group_by(Post.id) \
            .filter(Post.title.contains(search)) \
            .limit(limit).offset(skip) \
            .all()

    return posts 

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)) -> PostWithVotesResponse:

    post = db.query(Post, func.count(Vote.post_id).label("votes")) \
            .join(Vote, Vote.post_id == Post.id, isouter=True) \
            .group_by(Post.id) \
            .filter(Post.id == id) \
            .first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    
    return post


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: PostBase, 
                db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)
                ) -> PostResponse:
    new_post = Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}")
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):

    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to performed requestd action")

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, 
                payload: PostBase, 
                db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)
                ) -> PostResponse:

    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to performed requestd action")

    for k, v in payload.model_dump().items():
        if hasattr(post, k):
            setattr(post, k, v)

    db.commit()
    db.refresh(post)
    return post