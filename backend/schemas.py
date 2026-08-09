from pydantic import BaseModel, field_validator, Field
from typing import Optional, Literal



class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "from_attributes": True
    }




class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int

    model_config = {
        "from_attributes": True
    }



class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

    status: str = "pending"

    priority: Literal[
        "low",
        "medium",
        "high"
    ] = "medium"

    due_date: Optional[str] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Task title cannot be empty")

        return value


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    status: Optional[str] = None

    priority: Optional[
        Literal["low", "medium", "high"]
    ] = None

    due_date: Optional[str] = None
    project_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Task title cannot be empty")

        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    due_date: Optional[str] = None
    project_id: int

    model_config = {
        "from_attributes": True
    }




class QuickAddRequest(BaseModel):
    description: str = Field(..., min_length=1)
    project_id: int = Field(..., gt=0)

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        
        return value