from fastapi import FastAPI, Body
from schemas import Post

app = FastAPI()

@app.get("/")
async def root():
    return {"Ping": "Pong"}


@app.get("/posts")
async def get_posts():
    return {"data": "These are your posts"}


@app.post("/posts")
async def create_post(payload: Post):
    return payload