from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import engine, SessionLocal
import models

from routers import habits, tasks

import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from services.email_service import send_reminder_email

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit & Task Tracker")

app.include_router(habits.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    print("REMINDER LOOP STARTED")
    asyncio.create_task(reminder_loop())


# -------------------------------
# EMAIL REMINDER CHECKER
# -------------------------------

async def reminder_loop():
    while True:
        try:
            db = SessionLocal()

            current_time = datetime.now(
                ZoneInfo("Asia/Kolkata")
            ).strftime("%H:%M")

            print("SERVER TIME:", current_time)

            tasks_list = db.query(models.Task).filter(
                models.Task.is_done == False,
                models.Task.email_sent == False
            ).all()

            for task in tasks_list:

                print(
                    f"CHECKING -> {task.title} | Reminder={task.reminder_time} | Current={current_time}"
                )

                if (
                    task.reminder_time
                    and task.email
                    and task.reminder_time == current_time
                ):

                    print("MATCH FOUND")

                    print(
                        f"Sending reminder for {task.title} to {task.email}"
                    )

                    send_reminder_email(
                        task.email,
                        task.title
                    )

                    task.email_sent = True

            db.commit()
            db.close()

        except Exception as e:
            print("Reminder Error:", e)

        await asyncio.sleep(30)
