from app.schemas import PostWithVotesResponse, PostResponse


def test_get_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    assert res.status_code == 200
    assert len(res.json()) == 3


def test_create_post(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={"title": "title", "content": "content", "owner_id": test_user["id"]})

    created_post = PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.owner_id == test_user["id"]


def test_creat_post_without_auth(client):
    res = client.post("/posts/", json={"title": "title", "content": "content"})

    assert res.status_code == 401


def test_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    post = PostWithVotesResponse(**res.json())
    assert res.status_code == 200
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_post_non_exist(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/8000")      

    assert res.status_code == 404


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content"
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]  