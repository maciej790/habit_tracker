from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from .user import User 

class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    frequency: str
    is_active: bool = True
    start_date: date

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="habits")

    logs: List["HabitLog"] = Relationship(back_populates="habit")

class HabitLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date

    habit_id: int = Field(foreign_key="habit.id")
    habit: Habit = Relationship(back_populates="logs")
