from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    CheckConstraint
)

from sqlalchemy.orm import relationship

from .database import Base


# =========================================================
# USER MODEL
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    projects = relationship(
        "Project",
        back_populates="owner"
    )


# =========================================================
# PROJECT MODEL
# =========================================================

class Project(Base):
    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="projects"
    )

    tasks = relationship(
        "Task",
        back_populates="project"
    )


# =========================================================
# TASK MODEL
# =========================================================

class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (
        CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="ck_tasks_priority"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="pending"
    )

    priority = Column(
        String,
        nullable=False,
        default="medium"
    )

    due_date = Column(
        String,
        nullable=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )