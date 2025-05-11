def test_follow_user(client):
    user_to_follow = 2
    resp = client.post(f"/api/users/{user_to_follow}/follow", headers={"api-key": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] is True

def test_unfollow_user(client):
    user_to_unfollow = 2
    resp = client.delete(f"/api/users/{user_to_unfollow}/follow", headers={"api-key": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] is True

def test_get_me(client):
    resp = client.get("/api/users/me", headers={"api-key": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] is True
    assert "user" in data

def test_get_user_by_id(client):
    user_id = 2
    resp = client.get(f"/api/users/{user_id}", headers={"api-key": "test"})
    if resp.status_code == 404:
        pass
    elif resp.status_code == 200:
        data = resp.json()
        assert data["result"] is True
        assert "user" in data
