import pytest

@pytest.fixture()
def create_user(client):
    response = client.post("/auth/registration", json={"login": "test_login", "password": "test_password", "role": "Listener"})
    return response.json()

@pytest.fixture()
def create_user_presenter(create_user, client):
    client.put("/auth/change_role")
    return create_user

def test_registration(client):
    response = client.post("/auth/registration", json={"login": "test_login", "password": "test_password", "role": "Listener"})
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_registration_login_already_taken(create_user, client):
    response = client.post("/auth/registration", json={"login": "test_login", "password": "test_password", "role": "Listener"})
    assert response.status_code == 409
    assert response.json()["detail"] == 'Пользователь под таким именем уже существует'

def test_registration_incorrect_role(client):
    response = client.post("/auth/registration", json={"login": "test_login", "password": "test_password", "role": "Presenter"})
    assert response.status_code == 400
    assert response.json()["detail"] == 'Невозможно зарегистировать пользователя с данной ролью'

def test_login(create_user, client):
    user_id = create_user["user_id"]
    response = client.post("/auth/login", json={"login": "test_login", "password": "test_password"})
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

def test_login_incorrect_payload(create_user, client):
    response = client.post("/auth/login", json={"login": "Error", "password": "Error"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный логин или пароль"

def test_change_role(create_user, client):
    print(create_user["user_id"])
    response = client.put("/auth/change_role")
    print(response.json())
    assert response.json()["message"] == "Ваша роль: Presenter"

def test_change_role_unauthorized(client):
    response = client.put("/auth/change_role")
    assert response.status_code == 401
    assert response.json()["detail"] == "Пользователь не найден"

def test_logout(create_user, client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == 'Пользователь успешно вышел из системы'