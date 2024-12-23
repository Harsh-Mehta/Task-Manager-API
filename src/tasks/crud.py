from sqlalchemy.orm import Session

from src.tasks.models import Task
from src.tasks.schemas import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    completed: bool = None,
):
    query = db.query(Task)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    return query.offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.model_dump())

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if db_task:
        for key, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)

        db.commit()
        db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if db_task:
        db.delete(db_task)
        db.commit()

    return db_task
