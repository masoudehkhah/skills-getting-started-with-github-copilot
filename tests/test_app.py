"""Backend tests for the Mergington High School API (src/app.py).

All tests follow the AAA (Arrange-Act-Assert) pattern.
"""

from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activities = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activities


def test_get_activities_activity_structure(client):
    # Arrange
    required_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    for name, activity in response.json().items():
        assert required_keys.issubset(activity.keys()), f"{name} is missing fields"


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    assert activity_name in response.json()["message"]
    updated = client.get("/activities").json()
    assert email in updated[activity_name]["participants"]
    assert len(updated[activity_name]["participants"]) == initial_count + 1


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_without_email_returns_422(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


def test_duplicate_signup_is_allowed_current_behavior(client):
    # Arrange: the app performs no duplicate validation — document behavior as-is
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]
    initial_occurrences = activities[activity_name]["participants"].count(email)

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert activities[activity_name]["participants"].count(email) == initial_occurrences + 1
