# TaskFlow – Engineering Task Management Platform

TaskFlow is a full-stack task management application designed to manage engineering tasks efficiently. It provides a FastAPI-based backend, SQLite database, a web-based frontend, REST APIs, task prioritization, searching, sorting, and automated API testing.

## Features

- Create new tasks
- View all tasks
- Update existing tasks
- Delete tasks
- Track pending and completed tasks
- Priority management: Low, Medium, High
- Sort tasks based on priority
- Search tasks using Binary Search
- Search tasks using Linear Search
- Insertion Sort implementation
- SQLite database persistence
- REST API using FastAPI
- Responsive web dashboard
- Backend connection status
- Automated API testing using Pytest

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### Database
- SQLite

### Frontend
- HTML
- CSS
- JavaScript

### Testing
- Pytest
- FastAPI TestClient
- HTTPX

## Algorithms Implemented

TaskFlow includes custom implementations of fundamental algorithms.

### Insertion Sort
Used to arrange task records according to priority.

Priority ranking:

- Low = 1
- Medium = 2
- High = 3

### Binary Search
Used for efficient searching of tasks in sorted data.

### Linear Search
Used to search tasks sequentially and provides a simple comparison with binary search.

## Project Structure

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
├── requirements.txt
└── taskflow.db
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd TASKFLOW
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Backend

From the project root directory:

```bash
python -m uvicorn backend.main:app --reload
```

The backend will run locally on port `8000`.

FastAPI interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Running the Frontend

Open:

```text
frontend/index.html
```

using a local development server such as VS Code Live Server/Five Server.

The frontend communicates with the TaskFlow FastAPI backend.

## Running Tests

Run the API test suite from the project root:

```bash
python -m pytest backend/test_api.py -v
```

Current verified result:

```text
7 passed
```

Run the algorithm verification script with:

```bash
python -m backend.check_algorithms
```

The algorithm checks cover:

- Insertion Sort
- Binary Search
- Linear Search
- Not-found handling

## CRUD Operations

TaskFlow supports complete CRUD functionality:

- **Create** – Add a new task
- **Read** – Retrieve and display tasks
- **Update** – Modify an existing task
- **Delete** – Remove a task

CRUD operations are persisted using SQLite.

## API Capabilities

The backend provides endpoints for task management including:

- Retrieving tasks
- Creating tasks
- Updating tasks
- Deleting tasks
- Priority-based sorting
- Task searching

FastAPI Swagger documentation can be used to inspect and test the available endpoints.

## Testing Status

The project has been manually and automatically tested.

- Backend connection: Passed
- Create task: Passed
- Read tasks: Passed
- Update task: Passed
- Delete task: Passed
- Priority sorting: Passed
- Binary search: Passed
- Linear search: Passed
- Not-found handling: Passed
- Pytest API suite: 7 tests passed

## Future Improvements

- User authentication
- Multiple project dashboards
- Task filtering
- Deployment
- Improved due-date validation
- CI/CD integration

## Author

Shubham Kumar

---

TaskFlow – Engineering Operations Dashboard