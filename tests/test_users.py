import jwt
import pytest
from app.schemas import Token, UserResponse
from app.config import settings


email =  "helloworld@gmail.com" 
password = "testpassword"

wrong_email = "helloworldgmail.com"
wrong_password = "wrongpassword"


def test_create_user(client):
    res = client.post("/users", json={"email": email, "password": password})
    assert res.status_code == 201  
    user = UserResponse(**res.json())
    assert user.email == email


def test_login(test_user, client):
    res = client.post("/login", data={"username": email, "password": password})
    login_res = Token(**res.json())
    jwt_payload = jwt.decode(login_res.access_token, 
                             settings.jwt_secret_key, 
                             algorithms=[settings.jwt_algorithm])
    assert jwt_payload.get("user_id") == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    (wrong_email, password, 403),
    (email, wrong_password, 403),
    (wrong_email, wrong_password, 403)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", 
                      data={"username": email, "password": password})
    assert res.status_code == status_code
    assert res.json().get("detail") == "Invalid Credentials"

