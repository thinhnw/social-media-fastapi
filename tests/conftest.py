import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import oauth2
from app.database import get_db
from app.models import Base, Post
from app.main import app
from app.config import settings


engine = create_engine(settings.testdb_connection_str)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {"email": "helloworld@gmail.com", "password": "testpassword"}    
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()   
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user["id"]})


@pytest.fixture()   
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture()
def test_posts(test_user, session):
    posts_data = [
        {"title": "First title", "content": "First content", "owner_id": test_user["id"]},
        {"title": "Second title", "content": "Second content", "owner_id": test_user["id"]},
        {"title": "Third title", "content": "Third content", "owner_id": test_user["id"]}
    ]

    def create_post(post):
        return Post(**post)

    posts = list(map(create_post, posts_data))
    session.add_all(posts)
    session.commit()

    return posts
