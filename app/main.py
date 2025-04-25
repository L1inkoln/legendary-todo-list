from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, init_db, engine
from app.schemas import TodoCreate, TodoResponse
from app.crud import get_todos, create_todo


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация БД при старте
    await init_db()
    yield
    # Очистка при завершении
    await engine.dispose()


app = FastAPI(title="Legendary todo list", lifespan=lifespan)


@app.get("/todos", response_model=list[TodoResponse])
async def read_todos(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await get_todos(db, skip=skip, limit=limit)


@app.post("/todos", response_model=TodoResponse)
async def add_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await create_todo(db, todo.model_dump())
