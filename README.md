# TaskFlow --- Full-Stack Task Management Platform

TaskFlow is a full-stack task management application built with
**FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript**. It supports
user authentication, project-scoped tasks, task CRUD operations, custom
sorting and searching algorithms, and a deterministic natural-language
Quick Add feature.

The project runs locally and does not require a paid API or external AI
service.

## Features

-   User registration and login with hashed passwords and JWT access
    tokens
-   User-owned projects and project-scoped tasks
-   Create, view, update, and delete tasks
-   Pending/completed status and low/medium/high priorities
-   Priority sorting using a custom Insertion Sort implementation
-   Task lookup using Linear Search and Binary Search
-   Project-level task statistics
-   Quick Add: parse a task description into a title, priority, and
    due-date hint
-   SQLite persistence through SQLAlchemy
-   Responsive dashboard built with vanilla JavaScript, HTML, and CSS
-   Client-side validation and task caching
-   FastAPI request validation, error handling, CORS, and request timing
    logs
-   Automated API and authentication tests with Pytest

## Tech Stack

  Area             Technologies
  ---------------- ------------------------------------------------
  Backend          Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn
  Database         SQLite
  Frontend         HTML, CSS, JavaScript
  Authentication   JWT access tokens, hashed passwords
  Testing          Pytest, FastAPI TestClient
  Algorithms       Insertion Sort, Binary Search, Linear Search

## Project Structure

``` text
TASKFLOW/
├── backend/
│   ├── algorithms.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── quick_add.py
│   ├── schemas.py
│   ├── test_api.py
│   ├── test_auth.py
│   └── check_algorithms.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── benchmark_algorithms.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

``` powershell
git clone https://github.com/shubh519/TASKFLOW.git
cd TASKFLOW
```

### 2. Create and activate a virtual environment

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` powershell
python -m pip install -r requirements.txt
```

### 4. Configure the JWT signing key

Set a random key in the current PowerShell session before starting the
backend:

``` powershell
$env:TASKFLOW_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

Keep this key private. If you generate a new key, previously issued
tokens will no longer validate. Never commit secrets, `.env` files,
databases, or database backups.

### 5. Start the backend

From the project root:

``` powershell
python -m uvicorn backend.main:app --reload
```

-   API base URL: `http://127.0.0.1:8000`
-   Interactive API documentation: `http://127.0.0.1:8000/docs`

### 6. Start the frontend

Open a second terminal in the project root and run:

``` powershell
python -m http.server 5500 --directory frontend
```

Then open `http://127.0.0.1:5500`.

The frontend is configured to communicate with the local API on port
`8000`.

> **Existing database note:** If you have an older local SQLite database
> from before authentication was added, back it up before running any
> required migration. Do not repeatedly run migrations or delete the
> database as a troubleshooting shortcut.

## Authentication

1.  Create an account through the frontend registration form or
    `POST /auth/register`.
2.  Log in through the frontend or `POST /auth/login`.
3.  The API returns an access token on successful login.
4.  Protected requests use the `Authorization: Bearer <token>` header.
5.  Tasks are scoped to the authenticated user's projects.

The frontend stores its access token in `sessionStorage`. This is
suitable for a local learning/demo project; a production deployment
should additionally review HTTPS, XSS protections, rate limiting, and
secret management.

## Main API Endpoints

  ---------------------------------------------------------------------------------------
  Method                  Endpoint                                Purpose
  ----------------------- --------------------------------------- -----------------------
  `GET`                   `/`                                     API health/message

  `POST`                  `/auth/register`                        Register an account

  `POST`                  `/auth/login`                           Log in and receive a
                                                                  token

  `GET`                   `/projects`                             List the current user's
                                                                  projects

  `POST`                  `/projects`                             Create a project

  `GET`                   `/tasks`                                List tasks available to
                                                                  the current user

  `POST`                  `/tasks`                                Create a task

  `GET`                   `/tasks/{task_id}`                      Get a task

  `PUT`                   `/tasks/{task_id}`                      Update a task

  `DELETE`                `/tasks/{task_id}`                      Delete a task

  `GET`                   `/projects/{project_id}/stats`          Get project task
                                                                  statistics

  `GET`                   `/tasks/search?title=...&algo=linear`   Search tasks linearly

  `GET`                   `/tasks/search?title=...&algo=binary`   Search sorted task
                                                                  titles with Binary
                                                                  Search

  `POST`                  `/tasks/quick-add`                      Parse a description and
                                                                  create a task
  ---------------------------------------------------------------------------------------

Use `/docs` for the current request schemas and interactive endpoint
testing.

## Algorithms

### Insertion Sort

Used for custom priority sorting. Its time complexity is **O(n)** in the
best case and **O(n²)** in the worst case.

### Linear Search

Checks records sequentially. Its worst-case time complexity is **O(n)**
and it does not require sorted input.

### Binary Search

Searches records sorted by the relevant key. Its worst-case time
complexity is **O(log n)**.

The repository also includes algorithm comparison counting and a
benchmark script:

``` powershell
python benchmark_algorithms.py
python -m backend.check_algorithms
```

Benchmark timings and comparison counts depend on the input data and
implementation; use the included scripts to reproduce the results.

## Quick Add

The Quick Add endpoint (`POST /tasks/quick-add`) uses a **deterministic
local parser** to extract a task title, priority, and due-date hint from
a free-text description.

-   No external AI API or API key is required.
-   The same input follows the same parsing rules.
-   Recognized priority and date phrases influence the resulting task
    fields.
-   The created task is saved to the SQLite database.

This is rule-based parsing, not a live LLM integration.

## Run Tests

From the project root, with dependencies installed:

``` powershell
python -m pytest -v
```

The latest local test run recorded **20 passed**. It also emitted three
dependency deprecation warnings; no tests failed in that run. Run the
command again after making changes to confirm the current result.

## Security Notes

-   Passwords are stored as hashes rather than returned as plain text.
-   Protected API routes require a valid access token.
-   Project/task access is checked against user ownership.
-   Keep signing keys, passwords, `.env` files, SQLite databases, and
    database backups out of Git.
-   For production use, add deployment-specific security controls and
    review token storage.

## Future Improvements

Potential enhancements include cloud deployment, CI/CD, additional task
filters and dashboards, improved natural-language date handling, and
optional integration with a real LLM.

## Author

**Shubham Kumar**

------------------------------------------------------------------------

TaskFlow is a learning and portfolio project demonstrating REST API
development, database relationships, authentication, frontend/backend
integration, algorithm implementation, and automated testing.
