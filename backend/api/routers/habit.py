from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import APIRouter
from ..models.habit import Habit, HabitInOut, HabitUpdate
from services.auth import get_current_user
from config.database import get_session
from sqlmodel import Session, select
from typing import List

router = APIRouter()

router = APIRouter(
    prefix="/habit",
    #dependencies=[Depends(get_session)],
)

@router.post("/create", status_code=201)
async def create_new_habit(habit : HabitInOut, user = Depends(get_current_user), db: Session = Depends(get_session)):
    user_id = user.id
    existing_habit = db.exec(
        select(Habit).where(Habit.name == habit.name, Habit.user_id == user_id)
    ).first()

    if existing_habit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Habit with this name already exists for this user."
        )
        
    created_habit = Habit(**habit.model_dump(), user_id=user_id)
    db.add(created_habit)
    db.commit()
    db.refresh(created_habit)
    return created_habit

@router.get("/get_all_habits", status_code=200, response_model=List[HabitInOut])
async def get_all_habits(user = Depends(get_current_user), db: Session = Depends(get_session)):
    user_id = user.id
    habits = db.exec(
        select(Habit).where(Habit.user_id == user_id)
    ).all()
    
    return habits

@router.get("/get_habit_by_id/{habit_id}", status_code=200, response_model=HabitInOut)
async def get_habit_by_id(habit_id : int, user = Depends(get_current_user), db: Session = Depends(get_session)):
    user_id = user.id
    habit = db.exec(
        select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    ).first()
    
    return habit

@router.patch("/update/{habit_id}", status_code=200)
async def update_habit(habit : HabitUpdate, habit_id : int, user = Depends(get_current_user), db: Session = Depends(get_session)):
    habit_to_update = db.get(Habit, habit_id)
    if not habit_to_update:
        raise HTTPException(status_code=404, detail="Habit not found")
    habit_updated_data = habit.model_dump(exclude_unset=True)
    habit_to_update.sqlmodel_update(habit_updated_data)
    db.add(habit_to_update)
    db.commit()
    db.refresh(habit_to_update)
    return {"Habit updated sacessful!"}

@router.delete("/delete/{habit_id}", status_code=200)
async def delete_habit(habit_id : int, user = Depends(get_current_user), db: Session = Depends(get_session)):
    habit_to_delete = db.get(Habit, habit_id)
    if not habit_to_delete:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit_to_delete)
    db.commit()
    return {"Habit deleted sacessful!"}