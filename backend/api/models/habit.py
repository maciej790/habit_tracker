from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from .user import User 

class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    frequency: str #daily, weekly, mounthly
    is_active: bool = True
    start_date: date #now

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="habits")

    logs: List["HabitLog"] = Relationship(back_populates="habit")

class HabitLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date #date for check done habit

    habit_id: int = Field(foreign_key="habit.id")
    habit: Habit = Relationship(back_populates="logs")
    
class HabitInOut(BaseModel):
    name : str
    description: Optional[str] = None
    color: str
    icon: str
    frequency: str
    is_active: bool = True
    start_date: date
    
class HabitUpdate(BaseModel):
    name : str
    description: Optional[str] = None
    color: str
    icon: str
    frequency: str
    
    class Config:
        orm_mode = True