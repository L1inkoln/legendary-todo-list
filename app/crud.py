from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Todo


async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 25):
    result = await db.execute(select(Todo).offset(skip).limit(limit))
    return result.scalars().all()


async def create_todo(db: AsyncSession, todo_data: dict):
    todo = Todo(**todo_data)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo
