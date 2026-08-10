# TaskFlow – Full-Stack AI-Assisted Task Management Platform

TaskFlow is a full-stack engineering task management application built using FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript.

The application provides project and task management, persistent database storage, REST APIs, custom sorting and searching algorithms, responsive frontend functionality, automated testing, and an AI-assisted Quick Add feature implemented using a deterministic local parser.

The project runs locally and does not require a paid API, external AI service, or API key.

---

## Features

- Create and list users
- Create and list projects
- Create tasks
- View all tasks
- View individual tasks
- Update tasks
- Delete tasks
- Track pending and completed tasks
- Low, medium, and high task priorities
- Priority-based task sorting
- Binary Search for task lookup
- Linear Search for task lookup
- Custom Insertion Sort implementation
- Project-level task statistics
- SQLite database persistence
- FastAPI REST backend
- Responsive frontend dashboard
- LocalStorage task caching
- Client-side validation
- Backend error handling
- Request timing middleware
- FastAPI dependency injection
- CORS configuration
- AI-assisted Quick Add
- Deterministic natural-language task parser
- Automated API tests using Pytest
- Algorithm edge-case verification
- Algorithm comparison benchmarking

---

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

### Algorithms

- Insertion Sort
- Binary Search
- Linear Search

---

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
├── benchmark_algorithms.py
├── README.md
└── requirements.txt
```

---

## Database Design

TaskFlow uses three related database entities:

- `users`
- `projects`
- `tasks`

The main relationship structure is:

```text
User
  |
  | one-to-many
  v
Project
  |
  | one-to-many
  v
Task
```

A user can own multiple projects.

A project can contain multiple tasks.

`projects.owner_id` references `users.id`.

`tasks.project_id` references `projects.id`.

SQLAlchemy `relationship()` and `back_populates` are used to represent these relationships in the application models.

### User Fields

- `id`
- `name`
- `email`

The email field is unique and cannot be null.

### Project Fields

- `id`
- `name`
- `description`
- `owner_id`

`owner_id` is a foreign key referencing the user who owns the project.

### Task Fields

- `id`
- `title`
- `status`
- `priority`
- `due_date`
- `project_id`

`project_id` is a foreign key referencing the associated project.

The database contains a priority check constraint restricting priority to:

```text
low
medium
high
```

Required fields use `nullable=False`.

The due date is stored as text so natural-language values such as:

```text
tomorrow
next friday
next week
```

can be stored directly.

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TASKFLOW
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

TaskFlow uses a local frontend and backend setup.

### Start the Backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Start the Frontend

Serve the frontend directory using VS Code Live Server or Five Server.

Example frontend URL:

```text
http://127.0.0.1:5500/frontend/index.html
```

The frontend communicates with:

```text
http://127.0.0.1:8000
```

CORS middleware permits the local frontend origins required for development.

---

# REST API

## Root Endpoint

```http
GET /
```

Example response:

```json
{
  "message": "TaskFlow API is running"
}
```

---

## Users

### Create User

```http
POST /users
```

Example request:

```json
{
  "name": "Shubham Kumar",
  "email": "shubham@example.com"
}
```

Example response:

```json
{
  "id": 1,
  "name": "Shubham Kumar",
  "email": "shubham@example.com"
}
```

Successful creation returns:

```text
201 Created
```

### List Users

```http
GET /users
```

---

## Projects

### Create Project

```http
POST /projects
```

Example request:

```json
{
  "name": "TaskFlow",
  "description": "Engineering task management project",
  "owner_id": 1
}
```

Example response:

```json
{
  "id": 1,
  "name": "TaskFlow",
  "description": "Engineering task management project",
  "owner_id": 1
}
```

### List Projects

```http
GET /projects
```

---

## Project Statistics

```http
GET /projects/{project_id}/stats
```

Example:

```http
GET /projects/1/stats
```

Example response:

```json
{
  "project_id": 1,
  "total_tasks": 4,
  "pending": 3,
  "completed": 1
}
```

The statistics endpoint uses SQL aggregate functions through SQLAlchemy.

Task counts are calculated through database queries instead of fetching every task and manually counting all rows in Python.

---

# Task CRUD Operations

## Create Task

```http
POST /tasks
```

Example request:

```json
{
  "title": "Build Task CRUD API",
  "status": "pending",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1
}
```

Example response:

```json
{
  "id": 1,
  "title": "Build Task CRUD API",
  "status": "pending",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1
}
```

Successful creation returns:

```text
201 Created
```

---

## List Tasks

```http
GET /tasks
```

---

## Get Task by ID

```http
GET /tasks/{task_id}
```

Example:

```http
GET /tasks/1
```

A valid task returns:

```text
200 OK
```

A non-existing task returns:

```text
404 Not Found
```

---

## Update Task

```http
PUT /tasks/{task_id}
```

Example request:

```json
{
  "title": "Updated Task",
  "status": "completed",
  "priority": "high",
  "due_date": "next friday",
  "project_id": 1
}
```

A successful update returns:

```text
200 OK
```

---

## Delete Task

```http
DELETE /tasks/{task_id}
```

Example response:

```json
{
  "message": "Task deleted successfully"
}
```

A successful deletion returns:

```text
200 OK
```

---

# Priority Sorting

Tasks can be sorted by priority using:

```http
GET /tasks?sort=priority
```

Priority values are mapped internally as:

```text
low    = 1
medium = 2
high   = 3
```

The backend uses the custom:

```python
insertion_sort()
```

implementation to perform the ordering.

Python's built-in sorting functions are not used to perform the application-side priority sort.

---

# Task Searching

TaskFlow supports both Binary Search and Linear Search.

## Binary Search

```http
GET /tasks/search?title=Medium%20Priority%20Task&algo=binary
```

## Linear Search

```http
GET /tasks/search?title=Medium%20Priority%20Task&algo=linear
```

Binary Search is used when:

```text
algo=binary
```

Linear Search is used when:

```text
algo=linear
```

A matching task returns:

```text
200 OK
```

A missing task returns:

```text
404 Not Found
```

An unsupported algorithm value returns:

```text
422 Unprocessable Entity
```

---

# Algorithms

TaskFlow implements sorting and searching algorithms manually instead of relying only on Python's built-in operations.

## Insertion Sort

Function:

```python
insertion_sort(records, key)
```

Insertion Sort sorts a list of dictionaries according to the specified key.

### Time Complexity

Best case:

```text
O(n)
```

Worst case:

```text
O(n²)
```

Insertion Sort performs well for small or nearly sorted datasets.

Its performance decreases on large reverse-ordered datasets because many elements must be compared and shifted.

---

## Binary Search

Function:

```python
binary_search(sorted_records, target_value, key)
```

Binary Search operates on records already sorted by the requested key.

### Time Complexity

Best case:

```text
O(1)
```

Worst case:

```text
O(log n)
```

Binary Search is especially useful when repeated lookups are performed on sorted data.

TaskFlow creates a title index, sorts it using the custom Insertion Sort implementation, and then performs Binary Search.

---

## Linear Search

Function:

```python
linear_search(records, target_value, key)
```

Linear Search checks records sequentially.

### Time Complexity

Best case:

```text
O(1)
```

Worst case:

```text
O(n)
```

Linear Search requires no sorted input.

It can therefore be practical for small datasets or one-time searches.

---

# Algorithm Comparison Counting

TaskFlow also provides comparison-counting versions of its algorithms:

```python
insertion_sort_count(records, key)
binary_search_count(sorted_records, target_value, key)
linear_search_count(records, target_value, key)
```

These functions preserve the behavior of the algorithms while also reporting how many key comparisons were performed.

---

# Algorithm Benchmark

The benchmark can be executed using:

```bash
python benchmark_algorithms.py
```

The benchmark was run on reverse-ordered datasets containing:

```text
10 records
100 records
500 records
```

## Measured Results

| Dataset Size | Insertion Sort Comparisons | Linear Search Comparisons | Binary Search Comparisons |
|---:|---:|---:|---:|
| 10 | 45 | 10 | 4 |
| 100 | 4,950 | 100 | 7 |
| 500 | 124,750 | 500 | 9 |

## Benchmark Observations

Insertion Sort comparisons increased rapidly:

```text
10 records  -> 45 comparisons
100 records -> 4,950 comparisons
500 records -> 124,750 comparisons
```

This demonstrates the worst-case `O(n²)` behavior of Insertion Sort on reverse-ordered input.

Linear Search required:

```text
10 records  -> 10 comparisons
100 records -> 100 comparisons
500 records -> 500 comparisons
```

The target was positioned at the end of the sorted dataset, demonstrating worst-case `O(n)` behavior.

Binary Search required:

```text
10 records  -> 4 comparisons
100 records -> 7 comparisons
500 records -> 9 comparisons
```

This demonstrates the logarithmic `O(log n)` behavior of Binary Search.

The benchmark shows that Binary Search scales much better than Linear Search for lookups on sorted data, while Insertion Sort becomes expensive for large reverse-ordered datasets.

---

# Algorithm Verification

Run:

```bash
python -m backend.check_algorithms
```

The verification script covers:

- Insertion Sort with an empty list
- Insertion Sort with a single element
- Insertion Sort with unsorted records
- Binary Search first element
- Binary Search middle element
- Binary Search last element
- Binary Search not-found case
- Linear Search found cases
- Linear Search not-found case
- Insertion Sort comparison counter
- Binary Search comparison counter
- Binary Search counter not-found case
- Linear Search comparison counter
- Linear Search absent-target comparison count

Current verified result:

```text
Insertion Sort: PASS
Binary Search: PASS
Linear Search: PASS
Insertion Sort Count: PASS
Binary Search Count: PASS
Linear Search Count: PASS

ALL ALGORITHM TESTS PASSED
```

---

# AI-Assisted Quick Add

TaskFlow includes an AI-style Quick Add feature that converts a natural-language task description into structured task information.

Endpoint:

```http
POST /tasks/quick-add
```

The default implementation uses a deterministic local parser.

It requires:

```text
0 API keys
0 network calls
0 paid AI services
```

The parser extracts:

```text
title
priority
due_date_hint
```

The Quick Add endpoint converts the parsed result into a real Task record and stores it in the same SQLite database used by the rest of TaskFlow.

---

## Quick Add Request

Example request:

```json
{
  "description": "Finish the report next Friday, it's urgent",
  "project_id": 1
}
```

Example response:

```json
{
  "id": 5,
  "title": "Finish the report , it's",
  "status": "pending",
  "priority": "high",
  "due_date": "next friday",
  "project_id": 1
}
```

Successful creation returns:

```text
201 Created
```

The newly created task can subsequently be retrieved through:

```http
GET /tasks/{task_id}
```

This confirms that Quick Add persists the generated task in the database.

---

# Quick Add Validation

If the referenced project does not exist:

```json
{
  "description": "Finish assignment tomorrow urgent",
  "project_id": 999999
}
```

the API returns:

```text
422 Unprocessable Entity
```

with:

```text
Project not found
```

The invalid request does not create a task.

If the request body is malformed, for example:

```json
{
  "project_id": 1
}
```

the missing `description` field also produces:

```text
422 Unprocessable Entity
```

---

# Deterministic Quick Add Parsing

The Quick Add parser uses deterministic rules so the same input always produces the same output.

High-priority terms include:

```text
urgent
asap
high priority
```

Low-priority terms include:

```text
whenever
low priority
```

When no priority keyword matches, the default priority is:

```text
medium
```

Supported due-date phrases include values such as:

```text
today
tomorrow
next week
next monday
next tuesday
next wednesday
next thursday
next friday
next saturday
next sunday
monday
tuesday
wednesday
thursday
friday
saturday
sunday
```

Matched priority and date phrases are removed while constructing the task title.

If the resulting title contains only whitespace, the parser returns:

```text
Untitled task
```

---

# Prompting Technique Rationale

The AI-assisted Quick Add feature is modeled as a constrained zero-shot structured-extraction task. A system-style instruction defines the expected structured fields and parsing behavior, while the user's free-text task description acts as the input message.

For grading reliability and offline execution, TaskFlow uses a deterministic rule-based mock parser instead of requiring a real LLM. This keeps the interface similar to an LLM structured response while guaranteeing identical results for identical inputs, zero API-key requirements, zero network calls, and predictable validation behavior.

The parser extracts three values: `title`, `priority`, and `due_date_hint`. Priority is determined using ordered keyword groups. High- and low-priority terms are recognized, while `medium` is used when no priority term matches. Due-date phrases are also evaluated using deterministic matching rules. Recognized priority and date phrases are removed from the original description to construct the title.

This approach is closer to constrained structured prompting than chain-of-thought prompting. The application does not depend on exposing intermediate reasoning. Its purpose is to reliably transform free text into a small validated structured object.

A real LLM could later be placed behind the same interface as an optional enhancement while retaining the deterministic parser as the offline default.

---

# Quick Add Worked Examples

## Example 1

Input:

```text
This is urgent, mark it ASAP please
```

Parsed output:

```json
{
  "title": "This is , mark it please",
  "priority": "high",
  "due_date_hint": null
}
```

## Example 2

Input:

```text
Finish the report next Friday, it's urgent
```

Parsed output:

```json
{
  "title": "Finish the report , it's",
  "priority": "high",
  "due_date_hint": "next friday"
}
```

## Example 3

Input:

```text
tomorrow review tomorrow
```

Parsed output:

```json
{
  "title": "review",
  "priority": "medium",
  "due_date_hint": "tomorrow"
}
```

## Example 4

Input:

```text
   
```

Parsed output:

```json
{
  "title": "Untitled task",
  "priority": "medium",
  "due_date_hint": null
}
```

## Example 5

Input:

```text
low priority documentation next monday
```

Parsed output:

```json
{
  "title": "documentation",
  "priority": "low",
  "due_date_hint": "next monday"
}
```

---

# Frontend Dashboard

TaskFlow includes a responsive dashboard implemented using HTML, CSS, and JavaScript.

The frontend communicates with the real FastAPI backend using the Fetch API.

The interface supports:

- Viewing tasks
- Creating tasks
- Editing tasks
- Deleting tasks
- Refreshing tasks
- Displaying task priorities
- Displaying task status
- Displaying due dates
- Displaying project IDs
- Displaying total task count
- Displaying pending task count
- Displaying completed task count

---

# Client-Side Validation

The task form validates the title before sending a request.

Whitespace is trimmed using JavaScript.

If the title is empty, a visible error message is displayed:

```text
Task title is required.
```

The request is not sent until a valid title is provided.

The validation message is cleared when the user enters a valid title.

---

# LocalStorage Caching

TaskFlow uses browser `localStorage` to cache task data.

Tasks are stored using:

```javascript
JSON.stringify(tasks)
```

and restored using:

```javascript
JSON.parse(...)
```

When the page starts:

1. Cached tasks are loaded first when available.
2. Cached tasks are rendered immediately.
3. A request is then sent to the FastAPI backend for the latest data.
4. Successful backend data replaces the cached version.
5. If the backend is unavailable, cached tasks remain visible.

The cache is also updated after successful create, update, and delete operations.

---

# Responsive Design

TaskFlow uses CSS Grid and Flexbox for layout.

Two responsive breakpoints are implemented:

```text
768px
480px
```

At the tablet breakpoint, the task form changes from its desktop multi-column layout to a smaller grid.

At the mobile breakpoint:

- The top navigation changes to a vertical layout
- Statistics cards become a single column
- The task form becomes a single column
- Task cards become a single column
- Task action buttons reposition
- Section headings stack vertically

The header also uses a sticky position to remain visible during scrolling.

---

# Request Logging Middleware

TaskFlow includes custom HTTP middleware that measures request processing time.

For each request, information such as the following is logged:

```text
HTTP method
request path
processing time
```

Example:

```text
GET /tasks - 3.05 ms
```

---

# Dependency Injection

TaskFlow uses FastAPI:

```python
Depends()
```

to provide SQLAlchemy database sessions to route handlers.

The shared database dependency avoids duplicating database-session setup logic across endpoints.

---

# CORS

TaskFlow configures FastAPI CORS middleware for local frontend development.

Allowed origins include:

```text
http://localhost:5500
http://127.0.0.1:5500
```

This allows the frontend running on port `5500` to communicate with the FastAPI backend running on port `8000`.

---

# Input Validation

Pydantic models are used for request and response validation.

Task priority accepts only:

```text
low
medium
high
```

Task titles are stripped of surrounding whitespace.

A blank task title is rejected.

Malformed API request bodies return:

```text
422 Unprocessable Entity
```

The database also contains a priority check constraint as an additional data-integrity safeguard.

---

# Automated API Testing

Run the complete API test suite from the project root:

```bash
python -m pytest backend/test_api.py -v
```

Current verified result:

```text
15 passed, 3 warnings
```

The warnings do not represent failed tests.

The expanded API test suite verifies:

- Root endpoint
- Task listing
- Priority sorting
- Binary Search
- Linear Search
- Search not-found handling
- Invalid search algorithm handling
- Non-existing task handling
- Invalid task priority validation
- Blank task title validation
- Project statistics
- Complete task CRUD lifecycle
- Quick Add creation
- Quick Add database persistence
- Quick Add invalid-project validation
- Quick Add malformed-request validation

---

# Manual Verification

In addition to automated tests, TaskFlow has been manually tested through FastAPI Swagger and the frontend.

Verified functionality includes:

- Backend startup
- User endpoints
- Project endpoints
- Task creation
- Task retrieval
- Task update
- Task deletion
- Database persistence
- Priority sorting
- Binary Search
- Linear Search
- Search not-found handling
- Project statistics
- Quick Add creation
- Quick Add `201 Created`
- Quick Add database persistence
- Invalid project `422`
- Missing Quick Add description `422`

---

# HTTP Status Codes

Typical TaskFlow responses include:

```text
200 OK
201 Created
404 Not Found
422 Unprocessable Entity
```

---

# Git Workflow

Development uses Git for version control.

The AI-assisted Quick Add functionality was developed using the feature branch:

```text
feature/ai-quick-add
```

The feature branch contained multiple commits, including:

```text
Add deterministic quick-add parser and schemas
Complete AI quick-add feature
```

After testing, the feature branch was merged into:

```text
main
```

and pushed to the remote repository.

Git history can be inspected using:

```bash
git log --graph --oneline --all
```

---

# .gitignore

Generated and local development files are excluded where appropriate.

Examples include:

```text
.venv/
__pycache__/
*.pyc
taskflow.db
.pytest_cache/
```

---

# Final Testing Status

Current verified project testing status:

```text
Algorithm verification:
Insertion Sort: PASS
Binary Search: PASS
Linear Search: PASS
Insertion Sort Count: PASS
Binary Search Count: PASS
Linear Search Count: PASS
ALL ALGORITHM TESTS PASSED

Algorithm benchmark:
10 records  -> PASS
100 records -> PASS
500 records -> PASS

API test suite:
15 passed, 3 warnings
```

---

# Future Improvements

Possible future enhancements include:

- User authentication
- Additional project dashboards
- More task filters
- Cloud deployment
- CI/CD integration
- More advanced natural-language date parsing
- Optional real-LLM integration behind a disabled-by-default feature flag

The current application does not depend on these optional features to operate.

---

# Author

Shubham Kumar

---

**TaskFlow – Engineering Operations Dashboard**

A full-stack task management platform built using FastAPI, SQLAlchemy, SQLite, HTML, CSS, JavaScript, custom sorting/searching algorithms, and deterministic AI-assisted task parsing.

---

# Section 3 — Integrated AI Quick-Add

TaskFlow provides a Quick-Add feature that converts a free-text task
description into structured task information and stores the resulting task
in the same database used by the rest of the application.

## Quick-Add Endpoint

### POST /tasks/quick-add

Example request:

{
  "description": "Finish project next friday urgent",
  "project_id": 1
}

The endpoint parses the description and creates a real task associated with
the specified project.

Example response:

{
  "id": 1,
  "title": "Finish project",
  "status": "pending",
  "priority": "high",
  "due_date": "next friday",
  "project_id": 1
}

A successful request returns HTTP status code `201`.

If the request body is malformed or the supplied `project_id` does not
reference an existing project, the API returns HTTP `422` and does not create
a task.

---

## Prompt Structure

The Quick-Add feature uses the standard role-based structure used by LLM
messaging systems.

### System role

The system instruction describes the expected parsing behaviour. It instructs
the parser/model to convert a free-text task description into structured data
containing:

- title
- priority
- due_date_hint

### User role

The user message contains the original free-text task description that needs
to be parsed.

Keeping these roles separate means that the same interface can be used by the
deterministic mock parser and, optionally, by a real LLM implementation.

---

## Prompting Technique and Rationale

The Quick-Add design is primarily modelled on zero-shot prompting with explicit
rule-based instructions. The system message defines the required output
structure and parsing behaviour, while the user message contains only the task
description. The application does not require a model to learn the task from
previous conversation history.

For grading and normal execution, TaskFlow uses a deterministic mock parser.
The parser follows fixed keyword rules for priority and due-date extraction,
so the same input always produces the same output. This also makes the feature
usable without an API key, network connection, token usage, or paid AI
service.

The worked examples below resemble few-shot examples from a documentation
perspective because they demonstrate expected input-output behaviour. However,
the deterministic parser does not depend on these examples when executing.

This approach improves response reliability because parsing does not depend on
model randomness. It also eliminates token cost for the required baseline.
A real LLM could optionally be placed behind a feature flag, while the mock
parser remains the automatic fallback whenever the real model is disabled or
an API key is unavailable.

---

## Quick-Add Worked Examples

### Example 1

Input:

`This is urgent, mark it ASAP please`

Parsed output:

{
  "title": "This is , mark it  please",
  "priority": "high",
  "due_date_hint": null
}

### Example 2

Input:

`Finish the report next Friday, it's urgent`

Parsed output:

{
  "title": "Finish the report , it's",
  "priority": "high",
  "due_date_hint": "next friday"
}

### Example 3

Input:

`tomorrow review tomorrow`

Parsed output:

{
  "title": "review",
  "priority": "medium",
  "due_date_hint": "tomorrow"
}

### Example 4

Input:

`low priority documentation next monday`

Parsed output:

{
  "title": "documentation",
  "priority": "low",
  "due_date_hint": "next monday"
}

### Example 5

Input:

`whenever do this monday`

Parsed output:

{
  "title": "do this",
  "priority": "low",
  "due_date_hint": "monday"
}

### Example 6 — Empty Input

Input:

`   `

Parsed output:

{
  "title": "Untitled task",
  "priority": "medium",
  "due_date_hint": null
}

---

## Deterministic Mock Parser

The required baseline Quick-Add implementation makes:

- zero network calls
- zero external API calls
- zero paid-service calls
- zero API-key requirements

Priority values are restricted to:

`low`, `medium`, and `high`.

The mock parser is the default implementation used by
`POST /tasks/quick-add`.

---