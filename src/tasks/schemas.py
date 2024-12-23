from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


# Request Body Schemas

class TaskCreate(TaskBase):
    title: str


class TaskPartialUpdate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: str
    description: str = None
    completed: bool = False


class TaskFilter(BaseModel):
    completed: bool


# Response Body Schemas

class BaseResponse(BaseModel):
    status_code: int
    message: str


class TaskInDB(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskSingleResponse(BaseModel):
    status_code: int
    task: TaskInDB


class TaskListResponse(BaseModel):
    status_code: int
    tasks: list[TaskInDB]
