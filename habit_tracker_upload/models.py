from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import date

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    color = Column(String, default="#6366f1")
    created_at = Column(DateTime, server_default=func.now())
    completions = relationship("HabitCompletion", back_populates="habit", cascade="all, delete")

class HabitCompletion(Base):
    __tablename__ = "habit_completions"
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    completed_date = Column(Date, default=date.today)
    habit = relationship("Habit", back_populates="completions")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    is_done = Column(Boolean, default=False)
    priority = Column(String, default="medium")
    due_date = Column(Date, nullable=True)
    reminder_time = Column(String, nullable=True)

    email = Column(String, nullable=True)
    email_sent = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
