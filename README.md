# TaskFlow – A Full-Stack, AI-Assisted Task Management Platform

TaskFlow is a full-stack engineering task management application built for managing projects and tasks through a relational backend and a responsive web dashboard.

The application provides:

- Project and task management
- Persistent SQLite storage
- REST APIs using FastAPI
- Task creation, editing, deletion, and retrieval
- Project-level task statistics
- Custom insertion sort
- Custom binary search
- Custom linear search
- Priority-based task sorting
- Task searching
- AI-assisted Quick Add using a deterministic local parser
- Automated API testing using Pytest

The entire application runs locally and does not require a paid API or external AI service.

---

# Features

- Create users
- Create projects
- Create tasks
- View tasks
- Update tasks
- Delete tasks
- Track pending and completed tasks
- Low, medium, and high task priorities
- Sort tasks by priority
- Search tasks using binary search
- Search tasks using linear search
- Project task statistics
- Persistent SQLite database
- FastAPI REST backend
- Responsive frontend dashboard
- Backend connection status
- AI-assisted task Quick Add
- Deterministic natural-language task parser
- Automated API testing
- Algorithm verification script

---

# Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

## Database

- SQLite

## Frontend

- HTML
- CSS
- JavaScript

## Testing

- Pytest
- FastAPI TestClient
- HTTPX

## Algorithms

- Insertion Sort
- Binary Search
- Linear Search

| Dataset Size | Insertion Sort Comparisons | Linear Search Comparisons | Binary Search Comparisons |
|---:|---:|---:|---:|
| 10 | 45 | 10 | 4 |
| 100 | 4950 | 100 | 7 |
| 500 | 124750 | 500 | 9 |

---

# Project Structure

```text
TASKFLOW/
│
├── backend/
│   ├── __init__.py
│   ├── algorithms.py
│   ├── check_algorithms.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── quick_add.py
│   ├── schemas.py
│   └── test_api.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .gitignore
├── README.md
└── requirements.txt