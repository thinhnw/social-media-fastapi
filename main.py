from fastapi import FastAPI, Body
from schemas import Post
from database import db

app = FastAPI()

@app.get("/")
async def root():
    return {"Ping": "Pong"}


@app.get("/posts")
async def get_posts():
    return {"data": db["posts"]}


@app.get("/posts/{id}")
async def get_post(id: int):
    post = next((post for post in db["posts"] if post["id"] == id), None)  
    return post if post else {"error": "Post not found"} 


@app.post("/posts")
async def create_post(payload: Post):
    id = max(list(map(lambda post: post["id"], db["posts"]))) + 1
    db["posts"].append({
        **payload.model_dump(),
        "id": id
    })
    return db["posts"][-1]