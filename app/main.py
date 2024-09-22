from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from . import models
# from .config import settings
# from .database import engine
from .router import auth, posts, users, votes

# models.Base.metadata.create_all(bind=engine)
# use alembic to create the tables instead

app = FastAPI()

origins = ["https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API"}

