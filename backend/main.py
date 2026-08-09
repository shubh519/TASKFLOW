from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from .algorithms import insertion_sort, binary_search, linear_search
from sqlalchemy.orm import Session
from sqlalchemy import func
import time

from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    description="Backend API for TaskFlow Task Management Platform",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"- {process_time:.2f} ms"
    )

    return response


@app.get("/")
def root():
    return {
        "message": "TaskFlow API is running"
    }



@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    db_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()



@app.post("/projects", response_model=schemas.ProjectResponse, status_code=201)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        owner_id=project.owner_id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


@app.get("/projects", response_model=list[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()



@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    db_tasks = db.query(models.Task).all()

    task_records = []

    for task in db_tasks:
        task_records.append({
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "project_id": task.project_id
        })

    if sort == "priority":
        priority_rank = {
            "low": 1,
            "medium": 2,
            "high": 3
        }

        sortable_records = []

        for task in task_records:
            task_copy = task.copy()

            task_copy["priority_rank"] = priority_rank[
                task["priority"]
            ]

            sortable_records.append(task_copy)

        insertion_sort(
            sortable_records,
            "priority_rank"
        )

        for task in sortable_records:
            del task["priority_rank"]

        return sortable_records

    return task_records

@app.get(
    "/tasks/search",
    response_model=schemas.TaskResponse
)
def search_task(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db)
):
    db_tasks = db.query(models.Task).all()

    task_index = []

    for task in db_tasks:
        task_index.append({
            "id": task.id,
            "title": task.title
        })

    if algo == "binary":
        insertion_sort(
            task_index,
            "title"
        )

        result_index = binary_search(
            task_index,
            title,
            "title"
        )

    elif algo == "linear":
        result_index = linear_search(
            task_index,
            title,
            "title"
        )

    else:
        raise HTTPException(
            status_code=422,
            detail="algo must be binary or linear"
        )

    if result_index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task_id = task_index[result_index]["id"]

    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    return task
@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    updated_task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = updated_task.title
    task.status = updated_task.status
    task.priority = updated_task.priority
    task.due_date = updated_task.due_date
    task.project_id = updated_task.project_id

    db.commit()
    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }



@app.get("/projects/{project_id}/stats")
def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    total_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.project_id == project_id
    ).scalar()

    status_counts = db.query(
        models.Task.status,
        func.count(models.Task.id)
    ).filter(
        models.Task.project_id == project_id
    ).group_by(
        models.Task.status
    ).all()

    counts = {
        status_name: count
        for status_name, count in status_counts
    }

    return {
        "project_id": project_id,
        "total_tasks": total_tasks,
        "pending": counts.get("pending", 0),
        "completed": counts.get("completed", 0)
    }