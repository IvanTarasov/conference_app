import pytest
from .test_presentation import create_presentation
from .test_user import create_user_presenter, create_user

@pytest.fixture()
def create_schedule(create_presentation, client):
    response = client.post("/schedule/change_shedule_for_presentation", json={"date_time": "2024-12-31 23:00:00", "presentation_id": create_presentation["id"], "room_id": 1000})
    return response.json()

def test_get_all(create_schedule, client):
    response = client.get("/schedule/get_all")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_change_schedule_for_presentation(create_presentation, client):
    response = client.post("/schedule/change_shedule_for_presentation", json={"date_time": "2024-12-31 22:00:00", "presentation_id": create_presentation["id"], "room_id": 1000})
    data = response.json()
    assert response.status_code == 200
    assert data["date_time"] == "2024-12-31 22:00:00"
    assert data["room"] == "Unnamed"
    assert data["presentation"] == create_presentation["title"]

def test_change_schedule_for_presentation_filled_timeslot(create_schedule, client):
    response = client.post("/schedule/change_shedule_for_presentation", json={"date_time": create_schedule["date_time"], "presentation_id": create_schedule["presentation_id"], "room_id": 1000})
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Аудитория в это время занята"