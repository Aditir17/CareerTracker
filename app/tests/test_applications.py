import sys
sys.path.insert(0, r"C:\Users\admin\PycharmProjects\CareerTracker\app")

from fastapi.testclient import TestClient

from main import app
from dependencies import get_current_user

client = TestClient(app)


def test_application_dashboard_authenticated():
    app.dependency_overrides[get_current_user] = lambda: 1

    response = client.get("/applications/dashboard")

    assert response.status_code == 200

    data = response.json()

    assert "total_applications" in data
    assert "applied" in data
    assert "interview" in data
    assert "rejected" in data
    assert "offer" in data

    app.dependency_overrides.clear()

def test_application_dashboard_unauthenticated():
    app.dependency_overrides.clear()

    response = client.get("/applications/dashboard")

    assert response.status_code == 401

def test_create_application():
    app.dependency_overrides[get_current_user] = lambda: 3

    application_data = {
        "job_id": 2,
        "application_date": "2026-10-01",
        "status": "Applied",
        "notes": "Applied through company website"
    }

    response = client.post(
        "/applications/",
        json=application_data
    )

    assert response.status_code == 200

    data = response.json()
    assert data["job_id"] == 2
    assert data["status"] == "Applied"

    app.dependency_overrides.clear()

def test_create_application_invalid_job():
    app.dependency_overrides[get_current_user] = lambda: 1

    application_data = {
        "job_id": 99999,
        "application_date": "2026-10-01",
        "status": "Applied",
        "notes": "Test invalid job"
    }

    response = client.post(
        "/applications/",
        json=application_data
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"

    app.dependency_overrides.clear()

def test_get_application_by_id_unauthorized():
    app.dependency_overrides[get_current_user] = lambda: 1

    response = client.get("/applications/2")

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to view this application"

    app.dependency_overrides.clear()



