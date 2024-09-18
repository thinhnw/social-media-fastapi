from fastapi import FastAPI, Body, Response, status, HTTPException
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
async def get_post(id: int, response: Response):
    post = next((post for post in db["posts"] if post["id"] == id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return { "post": post }


@app.post("/posts")
async def create_post(payload: Post):
    id = max(list(map(lambda post: post["id"], db["posts"]))) + 1
    db["posts"].append({
        **payload.model_dump(),
        "id": id
    })
    return db["posts"][-1]


@app.delete("/posts/{id}")
async def delete_post(id: int):
    post = next((post for post in db["posts"] if post["id"] == id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    db["posts"].remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = next(
        (index for index, p in enumerate(db["posts"]) if p["id"] == id), 
        None
    )
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    db["posts"][index] = {
        **db["posts"][index],
        **post.model_dump()
    }
    return {
        "data": db["posts"][index]
    }