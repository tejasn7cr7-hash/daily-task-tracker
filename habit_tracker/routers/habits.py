from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Habit, HabitCompletion
from pydantic import BaseModel
from typing import Optional
from datetime import date

router = APIRouter(prefix="/habits", tags=["habits"])

class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    color: Optional[str] = "#6366f1"

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

@router.get("/")
def get_habits(db: Session = Depends(get_db)):
    habits = db.query(Habit).all()
    today = date.today()
    result = []
    for h in habits:
        completed_today = db.query(HabitCompletion).filter(
            HabitCompletion.habit_id == h.id,
            HabitCompletion.completed_date == today
        ).first() is not None

        # Calculate streak
        streak = 0
        check_date = today
        while True:
            done = db.query(HabitCompletion).filter(
                HabitCompletion.habit_id == h.id,
                HabitCompletion.completed_date == check_date
            ).first()
            if done:
                streak += 1
                check_date = date.fromordinal(check_date.toordinal() - 1)
            else:
                break

        total = db.query(HabitCompletion).filter(HabitCompletion.habit_id == h.id).count()
        result.append({
            "id": h.id,
            "name": h.name,
            "description": h.description,
            "color": h.color,
            "completed_today": completed_today,
            "streak": streak,
            "total_completions": total
        })
    return result

@router.post("/")
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = Habit(**habit.dict())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.put("/{habit_id}")
def update_habit(habit_id: int, habit: HabitUpdate, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    for k, v in habit.dict(exclude_none=True).items():
        setattr(db_habit, k, v)
    db.commit()
    return db_habit

@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(db_habit)
    db.commit()
    return {"ok": True}

@router.post("/{habit_id}/toggle")
def toggle_habit(habit_id: int, db: Session = Depends(get_db)):
    today = date.today()
    existing = db.query(HabitCompletion).filter(
        HabitCompletion.habit_id == habit_id,
        HabitCompletion.completed_date == today
    ).first()
    if existing:
        db.delete(existing)
        db.commit()
        return {"completed": False}
    else:
        completion = HabitCompletion(habit_id=habit_id, completed_date=today)
        db.add(completion)
        db.commit()
        return {"completed": True}
