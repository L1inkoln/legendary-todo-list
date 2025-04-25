from pydantic import BaseModel, Field
from typing import Optional


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)


class TodoCreate(TodoBase):
    completed: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    completed: Optional[bool] = None


class TodoResponse(TodoBase):
    id: int
    completed: bool = False

    class Config:
        from_attributes = True
