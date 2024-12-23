from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.tasks.crud import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task,
    update_task,
)
from src.tasks.schemas import (
    BaseResponse,
    TaskCreate,
    TaskListResponse,
    TaskUpdate,
    TaskPartialUpdate,
    TaskInDB,
    TaskFilter,
    TaskSingleResponse,
)
from src.tasks.utils import validate_string

router = APIRouter()


@router.get("/tasks", response_model=TaskListResponse, tags=["tasks"])
def get_tasks(db: Session = Depends(get_db), details: TaskFilter = None):
    """
    This endpoint retrieves all tasks. It also allows for filtering tasks by their completion status.

    If there are no tasks available, an empty list is returned."""

    if details:
        tasks = get_all_tasks(db=db, completed=details.completed)
    else:
        tasks = get_all_tasks(db=db)

    return {"status_code": 200, "tasks": tasks}


@router.get(
    "/tasks/{task_id}",
    response_model=TaskSingleResponse,
    tags=["tasks"],
    responses={404: {"description": "No task not found with ID provided"}},
)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """This endpoint returns the details of a task by its ID.
    
    **Errors:**
    - 404: If the task is not found. """

    task = get_task(db=db, task_id=task_id)

    if not task:
        raise HTTPException(
            status_code=404, detail="No task not found with ID provided"
        )

    return {"status_code": 200, "task": task}


@router.post(
    "/tasks",
    response_model=TaskInDB,
    tags=["tasks"],
    responses={
        400: {"description": "Invalid request body"},
        500: {"description": "Task not created"},
    },
)
def create_new_task(details: TaskCreate, db: Session = Depends(get_db)):
    """
    This endpoint creates a new task.

    **Errors:**
    - 400: If the request body is invalid.
    - 500: If the task has not been created.
    """

    details.title = details.title.strip()
    invalid = validate_string(details.title)

    if invalid:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty or only contain whitespace(s)",
        )

    task = create_task(db=db, task=details)

    if not task:
        raise HTTPException(status_code=500, detail="Task not created")

    return task


@router.put(
    "/tasks/{task_id}",
    response_model=TaskInDB,
    tags=["tasks"],
    responses={
        400: {"description": "Invalid request body"},
        404: {"description": "Unable to modify the task"},
    },
)
def modify_task(task_id: int, details: TaskUpdate, db: Session = Depends(get_db)):
    """This endpoint updates an existing task.

    **Errors:**
    - 400: If the request body is invalid.
    - 404: If the task has not been modified."""

    details.title = details.title.strip()
    invalid = validate_string(details.title)

    if invalid:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty or only contain whitespace(s)",
        )

    task = update_task(db=db, task_id=task_id, task=details)

    if not task:
        raise HTTPException(status_code=404, detail="Unable to update the task")

    return task


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskInDB,
    tags=["tasks"],
    responses={
        400: {"description": "Invalid request body"},
        404: {"description": "Unable to update the task"},
    },
)
def partial_update_task(
    task_id: int, details: TaskPartialUpdate, db: Session = Depends(get_db)
):
    """This endpoint partially updates the details an existing task.
    **Errors:**
    - 400: If the request body is invalid.
    - 404: If the details of the task have not been updated."""

    details.title = details.title.strip()
    invalid = validate_string(details.title)

    if invalid:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty or only contain whitespace(s)",
        )

    task = update_task(db=db, task_id=task_id, task=details)

    if task is None:
        raise HTTPException(status_code=404, detail="Unable to update the task")

    return task


@router.delete(
    "/tasks/{task_id}",
    response_model=BaseResponse,
    tags=["tasks"],
    responses={404: {"description": "Unable to delete the task"}},
)
def remove_task(task_id: int, db: Session = Depends(get_db)):
    """This endpoint deletes a task. If the task has not been deleted, a 404 error is returned."""

    task = delete_task(db=db, task_id=task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Unable to delete the task")

    return {"status_code": 200, "message": "Task has been deleted"}
