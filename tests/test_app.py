from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_initial_data():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    # Basic shape checks
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_adds_new_participant_and_prevents_duplicates():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Ensure clean state for this email
    participants = activities[activity_name]["participants"]
    if email in participants:
        participants.remove(email)

    # First signup should succeed
    first_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    assert first_response.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Second signup with same email should fail with 400
    second_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    assert second_response.status_code == 400
    error = second_response.json()
    assert "detail" in error


def test_remove_participant_from_activity():
    activity_name = "Programming Class"
    email = "remove_me@mergington.edu"

    participants = activities[activity_name]["participants"]
    if email not in participants:
        participants.append(email)

    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404():
    activity_name = "Gym Class"
    email = "not_registered@mergington.edu"

    participants = activities[activity_name]["participants"]
    if email in participants:
        participants.remove(email)

    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
