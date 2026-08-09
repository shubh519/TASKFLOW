from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Request,
)

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy import func

from pydantic import ValidationError

import time

from .database import Base, engine, get_db
from . import models, schemas

from .algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
)

from .quick_add import parse_task_description


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="TaskFlow API",
    description="Backend API for TaskFlow Task Management Platform",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Content-Type",
        "Accept",
    ],
)


# =========================================================
# REQUEST TIMING MIDDLEWARE
# =========================================================

@app.middleware("http")
async def log_request_time(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (
        time.perf_counter() - start_time
    ) * 1000

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"- {process_time:.2f} ms"
    )

    return response


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "TaskFlow API is running"
    }


# =========================================================
# USERS
# =========================================================

@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(models.User)
        .filter(
            models.User.email == user.email
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    db_user = models.User(
        name=user.name,
        email=user.email,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get(
    "/users",
    response_model=list[schemas.UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
):
    return db.query(models.User).all()


# =========================================================
# PROJECTS
# =========================================================

@app.post(
    "/projects",
    response_model=schemas.ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    owner = (
        db.query(models.User)
        .filter(
            models.User.id == project.owner_id
        )
        .first()
    )

    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner user not found",
        )

    db_project = models.Project(
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


@app.get(
    "/projects",
    response_model=list[schemas.ProjectResponse],
)
def get_projects(
    db: Session = Depends(get_db),
):
    return db.query(models.Project).all()


# =========================================================
# CREATE TASK
# =========================================================

@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == task.project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    db_task = models.Task(
        **task.model_dump()
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


# =========================================================
# AI QUICK ADD
#
# IMPORTANT:
# Must stay BEFORE /tasks/{task_id}
# =========================================================

@app.post(
    "/tasks/quick-add",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def quick_add_task(
    quick_task: schemas.QuickAddRequest,
    db: Session = Depends(get_db),
):
    # -----------------------------------------
    # Check project
    # -----------------------------------------

    project = (
        db.query(models.Project)
        .filter(
            models.Project.id
            == quick_task.project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "type": "value_error",
                    "loc": [
                        "body",
                        "project_id",
                    ],
                    "msg": "Project not found",
                    "input": quick_task.project_id,
                }
            ],
        )

    # -----------------------------------------
    # Deterministic mock parser
    # Zero API key / zero network
    # -----------------------------------------

    parsed = parse_task_description(
        quick_task.description
    )

    # -----------------------------------------
    # Validate parsed task
    # -----------------------------------------

    validated_task = schemas.TaskCreate(
        title=parsed["title"],
        status="pending",
        priority=parsed["priority"],
        due_date=parsed["due_date_hint"],
        project_id=quick_task.project_id,
    )

    # -----------------------------------------
    # Validate response-shaped object
    # BEFORE database persistence
    # -----------------------------------------

    try:
        schemas.TaskResponse.model_validate(
            {
                "id": 0,
                "title": validated_task.title,
                "status": validated_task.status,
                "priority": validated_task.priority,
                "due_date": validated_task.due_date,
                "project_id": validated_task.project_id,
            }
        )

    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error.errors(),
        )

    # -----------------------------------------
    # Persist only after validation succeeds
    # -----------------------------------------

    db_task = models.Task(
        **validated_task.model_dump()
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


# =========================================================
# LIST TASKS + INSERTION SORT
# =========================================================

@app.get(
    "/tasks",
    response_model=list[schemas.TaskResponse],
)
def get_tasks(
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    db_tasks = (
        db.query(models.Task)
        .all()
    )

    task_records = []

    for task in db_tasks:
        task_records.append(
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "project_id": task.project_id,
            }
        )

    if sort == "priority":
        priority_rank = {
            "low": 1,
            "medium": 2,
            "high": 3,
        }

        sortable_records = []

        for task in task_records:
            task_copy = task.copy()

            task_copy["priority_rank"] = (
                priority_rank[
                    task["priority"]
                ]
            )

            sortable_records.append(
                task_copy
            )

        insertion_sort(
            sortable_records,
            "priority_rank",
        )

        for task in sortable_records:
            del task["priority_rank"]

        return sortable_records

    return task_records


# =========================================================
# SEARCH TASKS
#
# IMPORTANT:
# Must stay BEFORE /tasks/{task_id}
# =========================================================

@app.get(
    "/tasks/search",
    response_model=schemas.TaskResponse,
)
def search_task(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db),
):
    db_tasks = (
        db.query(models.Task)
        .all()
    )

    task_index = []

    for task in db_tasks:
        task_index.append(
            {
                "id": task.id,
                "title": task.title,
            }
        )

    if algo == "binary":
        insertion_sort(
            task_index,
            "title",
        )

        result_index = binary_search(
            task_index,
            title,
            "title",
        )

    elif algo == "linear":
        result_index = linear_search(
            task_index,
            title,
            "title",
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="algo must be binary or linear",
        )

    if result_index == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task_id = task_index[
        result_index
    ]["id"]

    task = (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id
        )
        .first()
    )

    return task


# =========================================================
# GET TASK BY ID
# =========================================================

@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


# =========================================================
# UPDATE TASK
# =========================================================

@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
)
def update_task(
    task_id: int,
    updated_task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    task = (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    project = (
        db.query(models.Project)
        .filter(
            models.Project.id
            == updated_task.project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    task.title = updated_task.title
    task.status = updated_task.status
    task.priority = updated_task.priority
    task.due_date = updated_task.due_date
    task.project_id = updated_task.project_id

    db.commit()
    db.refresh(task)

    return task


# =========================================================
# DELETE TASK
# =========================================================

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }


# =========================================================
# PROJECT STATISTICS
# SQL JOIN + COUNT + GROUP BY
# =========================================================

@app.get("/projects/{project_id}/stats")
def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    total_tasks = (
        db.query(
            func.count(models.Task.id)
        )
        .select_from(models.Project)
        .outerjoin(
            models.Task,
            models.Project.id
            == models.Task.project_id,
        )
        .filter(
            models.Project.id
            == project_id
        )
        .scalar()
    )

    status_counts = (
        db.query(
            models.Task.status,
            func.count(models.Task.id),
        )
        .select_from(models.Project)
        .outerjoin(
            models.Task,
            models.Project.id
            == models.Task.project_id,
        )
        .filter(
            models.Project.id
            == project_id
        )
        .group_by(
            models.Task.status
        )
        .all()
    )

    counts = {
        status_name: count
        for status_name, count
        in status_counts
        if status_name is not None
    }

    return {
        "project_id": project_id,
        "total_tasks": total_tasks,
        "pending": counts.get(
            "pending",
            0,
        ),
        "completed": counts.get(
            "completed",
            0,
        ),
    }