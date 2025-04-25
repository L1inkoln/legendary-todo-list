from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Todo


async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 25):
    """Получение списка задач"""
    result = await db.execute(select(Todo).offset(skip).limit(limit))
    return result.scalars().all()


async def get_todo_by_id(db: AsyncSession, todo_id: int):
    """Получение одной задачи по ID"""
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalars().first()


async def create_todo(db: AsyncSession, todo_data: dict):
    """Создание новой задачи"""
    todo = Todo(**todo_data)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(db: AsyncSession, todo_id: int, todo_data: dict):
    """Обновление задачи"""
    stmt = update(Todo).where(Todo.id == todo_id).values(**todo_data)
    await db.execute(stmt)
    await db.commit()
    return await get_todo_by_id(db, todo_id)


async def delete_todo(db: AsyncSession, todo_id: int):
    """Удаление задачи"""
    stmt = delete(Todo).where(Todo.id == todo_id)
    await db.execute(stmt)
    await db.commit()
    return {"message": "Task deleted"}
