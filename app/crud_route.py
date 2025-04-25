from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.crud import get_todos, get_todo_by_id, create_todo, update_todo, delete_todo
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Tasks"])


# CRUD endpoints для todo
@router.get("/todos", response_model=list[TodoResponse])
async def read_todos(
    skip: int = 0, limit: int = 25, db: AsyncSession = Depends(get_db)
):
    logger.info(f"Getting todos, skip={skip}, limit={limit}")
    return await get_todos(db, skip=skip, limit=limit)


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Getting todo ID: {todo_id}")
    todo = await get_todo_by_id(db, todo_id)
    if not todo:
        logger.warning(f"Todo not found, ID: {todo_id}")
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def add_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating new todo: {todo.title}")
    created_todo = await create_todo(db, todo.model_dump())
    logger.info(f"Created todo ID: {created_todo.id}")
    return created_todo


@router.patch("/todos/{todo_id}", response_model=TodoResponse)
async def edit_todo(todo_id: int, todo: TodoUpdate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Updating todo ID: {todo_id}")
    existing_todo = await get_todo_by_id(db, todo_id)
    if not existing_todo:
        logger.warning(f"Todo not found for update, ID: {todo_id}")
        raise HTTPException(status_code=404, detail="Todo not found")

    updated_todo = await update_todo(db, todo_id, todo.model_dump(exclude_unset=True))
    logger.info(f"Updated todo ID: {todo_id}")
    return updated_todo


@router.delete("/todos/{todo_id}")
async def remove_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting todo ID: {todo_id}")
    existing_todo = await get_todo_by_id(db, todo_id)
    if not existing_todo:
        logger.warning(f"Todo not found for deletion, ID: {todo_id}")
        raise HTTPException(status_code=404, detail="Todo not found")

    await delete_todo(db, todo_id)
    logger.info(f"Deleted todo ID: {todo_id}")
    return {"message": "Todo deleted"}
