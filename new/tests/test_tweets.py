import pytest

def test_create_tweet(client):
    response = client.post(
        "/api/tweets",
        headers={"api-key": "test"},
        json={"tweet_data": "Hello from test!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "tweet_id" in data

def test_delete_tweet(client):
    create_resp = client.post(
        "/api/tweets",
        headers={"api-key": "test"},
        json={"tweet_data": "I will be deleted!"}
    )
    tweet_id = create_resp.json()["tweet_id"]
    delete_resp = client.delete(f"/api/tweets/{tweet_id}", headers={"api-key": "test"})
    assert delete_resp.status_code == 200
    assert delete_resp.json()["result"] is True

def test_like_unlike_tweet(client):
    create_resp = client.post(
        "/api/tweets",
        headers={"api-key": "test"},
        json={"tweet_data": "Like me!"}
    )
    tweet_id = create_resp.json()["tweet_id"]

    like_resp = client.post(f"/api/tweets/{tweet_id}/likes", headers={"api-key": "test"})
    assert like_resp.status_code == 200
    assert like_resp.json()["result"] is True

    unlike_resp = client.delete(f"/api/tweets/{tweet_id}/likes", headers={"api-key": "test"})
    assert unlike_resp.status_code == 200
    assert unlike_resp.json()["result"] is True

def test_get_tweets(client):
    resp = client.get("/api/tweets", headers={"api-key": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] is True
    assert "tweets" in data
    assert isinstance(data["tweets"], list)
