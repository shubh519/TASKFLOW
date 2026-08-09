from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "TaskFlow API is running"


def test_sort_tasks_by_priority():
    response = client.get("/tasks?sort=priority")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_binary_search_task():
    response = client.get(
        "/tasks/search",
        params={
            "title": "Medium Priority Task",
            "algo": "binary"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Medium Priority Task"


def test_linear_search_task():
    response = client.get(
        "/tasks/search",
        params={
            "title": "Medium Priority Task",
            "algo": "linear"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Medium Priority Task"


def test_search_task_not_found():
    response = client.get(
        "/tasks/search",
        params={
            "title": "ABCXYZ123",
            "algo": "binary"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_task_crud():
    # CREATE
    create_response = client.post(
        "/tasks",
        json={
            "title": "Pytest CRUD Task",
            "status": "pending",
            "priority": "medium",
            "due_date": "tomorrow",
            "project_id": 1
        }
    )

    assert create_response.status_code == 201

    created_task = create_response.json()
    task_id = created_task["id"]

    assert created_task["title"] == "Pytest CRUD Task"

    # READ
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id

    # UPDATE
    update_response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated Pytest Task",
            "status": "completed",
            "priority": "high",
            "due_date": "next friday",
            "project_id": 1
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Pytest Task"
    assert update_response.json()["status"] == "completed"

    # DELETE
    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully"

    # VERIFY DELETE
    final_response = client.get(f"/tasks/{task_id}")

    assert final_response.status_code == 404