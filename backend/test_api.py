from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "TaskFlow API is running"


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_sort_tasks_by_priority():
    response = client.get("/tasks?sort=priority")

    assert response.status_code == 200

    tasks = response.json()

    assert isinstance(tasks, list)

    priority_rank = {
        "low": 1,
        "medium": 2,
        "high": 3
    }

    ranks = [
        priority_rank[task["priority"]]
        for task in tasks
    ]

    assert ranks == sorted(ranks)


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


def test_invalid_search_algorithm():
    response = client.get(
        "/tasks/search",
        params={
            "title": "Medium Priority Task",
            "algo": "jump"
        }
    )

    assert response.status_code == 422


def test_get_missing_task():
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_invalid_task_priority():
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid Priority Task",
            "status": "pending",
            "priority": "super-high",
            "due_date": None,
            "project_id": 1
        }
    )

    assert response.status_code == 422


def test_blank_task_title():
    response = client.post(
        "/tasks",
        json={
            "title": "   ",
            "status": "pending",
            "priority": "medium",
            "due_date": None,
            "project_id": 1
        }
    )

    assert response.status_code == 422


def test_project_stats():
    response = client.get("/projects/1/stats")

    assert response.status_code == 200

    data = response.json()

    assert data["project_id"] == 1
    assert "total_tasks" in data
    assert "pending" in data
    assert "completed" in data


def test_task_crud():
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

    get_response = client.get(
        f"/tasks/{task_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id

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

    delete_response = client.delete(
        f"/tasks/{task_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully"

    final_response = client.get(
        f"/tasks/{task_id}"
    )

    assert final_response.status_code == 404


def test_quick_add_success_and_persistence():
    response = client.post(
        "/tasks/quick-add",
        json={
            "description": "Finish quick test tomorrow urgent",
            "project_id": 1
        }
    )

    assert response.status_code == 201

    created_task = response.json()

    assert created_task["priority"] == "high"
    assert created_task["due_date"] == "tomorrow"
    assert created_task["project_id"] == 1

    task_id = created_task["id"]

    get_response = client.get(
        f"/tasks/{task_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id

    client.delete(
        f"/tasks/{task_id}"
    )


def test_quick_add_invalid_project():
    response = client.post(
        "/tasks/quick-add",
        json={
            "description": "Finish assignment tomorrow urgent",
            "project_id": 999999
        }
    )

    assert response.status_code == 422


def test_quick_add_missing_description():
    response = client.post(
        "/tasks/quick-add",
        json={
            "project_id": 1
        }
    )

    assert response.status_code == 422