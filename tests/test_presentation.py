import pytest
from .test_user import create_user_presenter, create_user

@pytest.fixture()
def create_presentation(create_user_presenter, client):
    response = client.post("/presentation/create", json={"title": "Test"})
    return response.json()

def test_create_presentation(create_user_presenter, client):
    response = client.post("/presentation/create", json={"title": "Test"})
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Test"
    assert "id" in data
    assert data["room"] == "Не назначена"
    assert data["date_time"] == "Не выбрано"

def test_create_presentation_already_taken(create_presentation, client):
    response = client.post("/presentation/create", json={"title": "Test"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Такая презентация уже существует"

def test_presentation_wrong_role(create_user, client):
    response = client.post("/presentation/create", json={"title": "Test"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Операции с презентациями вам не доступны"

def test_get_my(create_presentation, client):
    response = client.get("/presentation/get_my")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_update_presentation(create_presentation, client):
    response = client.put("/presentation/update", json={"title": "new title","id": create_presentation["id"]})
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "new title"
    assert data["id"] == create_presentation["id"]
    assert data["room"] == create_presentation["room"]
    assert data["date_time"] == create_presentation["date_time"]

def test_update_presentation_wrong_id(create_presentation, client):
    response = client.put("/presentation/update", json={"title": "new title","id": 0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Презентация отсутствует или вам не принадлежит"

def test_delete_presentation(create_presentation, client):
    response = client.delete(f"/presentation/delete?presentation_id={create_presentation["id"]}")
    assert response.status_code == 200
    assert response.json()["message"] == "Удалено записей: 1"

def test_delete_presentation_wrong_id(create_presentation, client):
    response = client.delete(f"/presentation/delete?presentation_id=0")
    assert response.status_code == 400
    assert response.json()["detail"] == "Презентация отсутствует или вам не принадлежит"