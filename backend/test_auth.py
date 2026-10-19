"""Focused tests for JWT authentication and user/project isolation."""

from uuid import uuid4

from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


def _register_user(name="JWT Test User"):
    email = f"jwt-{uuid4().hex}@example.test"
    response = client.post(
        "/auth/register",
        json={"name": name, "email": email, "password": "SafeTestPass123!"},
    )
    assert response.status_code == 201, response.text
    return {"name": name, "email": email, "password": "SafeTestPass123!"}


def _login(user):
    response = client.post(
        "/auth/login",
        json={"email": user["email"], "password": user["password"]},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def test_protected_tasks_reject_missing_token():
    response = client.get("/tasks")
    assert response.status_code == 401


def test_register_login_and_duplicate_registration():
    user = _register_user()
    duplicate = client.post("/auth/register", json=user)
    assert duplicate.status_code == 409

    token = _login(user)
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == user["email"]


def test_login_rejects_wrong_password():
    user = _register_user()
    response = client.post(
        "/auth/login",
        json={"email": user["email"], "password": "WrongPassword123!"},
    )
    assert response.status_code == 401


def test_malformed_token_is_rejected():
    response = client.get(
        "/tasks",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert response.status_code == 401


def test_user_can_only_access_owned_projects_and_tasks():
    user_a = _register_user("Owner A")
    token_a = _login(user_a)
    headers_a = {"Authorization": f"Bearer {token_a}"}

    project_response = client.post(
        "/projects",
        headers=headers_a,
        json={
            "name": "JWT isolated project",
            "description": "Auth test project",
            "owner_id": client.get("/users", headers=headers_a).json()[0]["id"],
        },
    )
    assert project_response.status_code == 201, project_response.text
    project = project_response.json()

    task_response = client.post(
        "/tasks",
        headers=headers_a,
        json={
            "title": "JWT protected task",
            "status": "pending",
            "priority": "medium",
            "due_date": None,
            "project_id": project["id"],
        },
    )
    assert task_response.status_code == 201, task_response.text
    task = task_response.json()

    user_b = _register_user("Owner B")
    token_b = _login(user_b)
    headers_b = {"Authorization": f"Bearer {token_b}"}

    assert client.get(f"/tasks/{task['id']}", headers=headers_b).status_code == 403
    assert client.get("/projects", headers=headers_b).json() == []

    forbidden_project = client.post(
        "/projects",
        headers=headers_b,
        json={
            "name": "Forged ownership",
            "description": "Must be rejected",
            "owner_id": project["owner_id"],
        },
    )
    assert forbidden_project.status_code == 403
