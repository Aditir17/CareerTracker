import sys
sys.path.insert(0, r"C:\Users\admin\PycharmProjects\CareerTracker\app")

from fastapi.testclient import TestClient

from main import app
from dependencies import get_current_user

client = TestClient(app)


def test_create_job():
    app.dependency_overrides[get_current_user] = lambda: 1

    job_data = {
        "title": "Python Developer",
        "description": "Backend development role",
        "location": "Pune",
        "company_id": 1,
        "status": "Open"
    }

    response = client.post(
        "/jobs/",
        json=job_data
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Python Developer"
    assert data["company_id"] == 1
    assert data["status"] == "Open"

    app.dependency_overrides.clear()

def test_create_job_invalid_company():
    app.dependency_overrides[get_current_user] = lambda: 1

    job_data = {
        "title": "Python Developer",
        "description": "Backend development role",
        "location": "Pune",
        "company_id": 99999,
        "status": "Open"
    }

    response = client.post(
        "/jobs/",
        json=job_data
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found"

    app.dependency_overrides.clear()


def test_create_job():
    app.dependency_overrides[get_current_user] = lambda: 1

    job_data = {
        "title": "Python Developer",
        "description": "Backend development role",
        "location": "Pune",
        "company_id": 1,
        "status": "Open"
    }

    response = client.post(
        "/jobs/",
        json=job_data
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Python Developer"
    assert data["company_id"] == 1
    assert data["status"] == "Open"

    app.dependency_overrides.clear()

def test_create_job_invalid_company():
    app.dependency_overrides[get_current_user] = lambda: 1

    job_data = {
        "title": "Python Developer",
        "description": "Backend development role",
        "location": "Pune",
        "company_id": 99999,
        "status": "Open"
    }

    response = client.post(
        "/jobs/",
        json=job_data
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found"

    app.dependency_overrides.clear()
