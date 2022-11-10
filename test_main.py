from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World"}

def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "secret_token"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }

def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "fake_token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_read_inexistent_item():
    response = client.get("/items/gaz", headers={"X-Token": "secret_token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_item():
    response = client.post(
        "/items/", 
        headers={"X-Token": "secret_token"},
        json={"id": "bats", "title": "Batman", "description": "Bruce Wayne is not the Batman?!"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": "bats", "title": "Batman", "description": "Bruce Wayne is not the Batman?!"}

def test_create_item_bad_token():
    response = client.post(
        "/items/", 
        headers={"X-Token": "fake_token"},
        json={"id": "bats", "title": "Batman", "description": "Bruce Wayne is not the Batman?!"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_create_existing_item():
    response = client.post(
        "/items/", 
        headers={"X-Token": "secret_token"},
        json={"id": "foo", "title": "Foo Returns", "description": "This is a Fake Foo"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}