def test_vote(test_user, test_posts, authorized_client):
    res = authorized_client.post(
        "/votes/", json={"post_id": test_posts[0].id}
    )

    assert res.status_code == 201