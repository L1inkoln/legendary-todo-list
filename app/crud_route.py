from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.crud import get_todos, get_todo_by_id, create_todo, update_todo, delete_todo

router = APIRouter(tags=["Tasks"])


@router.get("/todos", response_model=list[TodoResponse])
async def read_todos(
    skip: int = 0, limit: int = 25, db: AsyncSession = Depends(get_db)
):
    return await get_todos(db, skip=skip, limit=limit)


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await get_todo_by_id(db, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def add_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await create_todo(db, todo.model_dump())


@router.patch("/todos/{todo_id}", response_model=TodoResponse)
async def edit_todo(todo_id: int, todo: TodoUpdate, db: AsyncSession = Depends(get_db)):
    existing_todo = await get_todo_by_id(db, todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo.model_dump(exclude_unset=True)
    return await update_todo(db, todo_id, update_data)


@router.delete("/todos/{todo_id}")
async def remove_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    existing_todo = await get_todo_by_id(db, todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return await delete_todo(db, todo_id)
