from fastapi import FastAPI
from . import models
# from .config import settings
# from .database import engine
from .router import auth, posts, users, votes

# models.Base.metadata.create_all(bind=engine)
# use alembic to create the tables instead

app = FastAPI()

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)

