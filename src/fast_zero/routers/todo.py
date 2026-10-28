from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.types import Message

from fast_zero.database import get_session
from fast_zero.models import Todo, TodoState, User
from fast_zero.schemas import TodoList, TodoPublic, TodoSchema, TodoUpdate
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


class TodoFilterParams(BaseModel):
    title: str | None = Query(default=None)
    description: str | None = Query(default=None)
    state: TodoState | None = Query(default=None)
    offset: int | None = Query(default=0, ge=0)
    limit: int | None = Query(default=10, le=100)


FilterParams = Annotated[TodoFilterParams, Depends()]


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: CurrentUser, session: Session):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(session: Session, user: CurrentUser, todo_filter: FilterParams):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = session.scalars(
        query.offset(todo_filter.offset).limit(todo_filter.limit)
    ).all()

    return {'todos': todos}


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: Session, user: CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, session: Session, user: CurrentUser, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
