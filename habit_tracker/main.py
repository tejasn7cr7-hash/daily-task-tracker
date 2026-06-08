from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine
import models
from routers import habits, tasks
import threading
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Daily Task Tracker")

app.include_router(habits.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# ── Background email reminder scheduler ──
def reminder_scheduler():
    print("✅ Email reminder scheduler started!")
    while True:
        try:
            from email_reminder import check_and_send_reminders
            check_and_send_reminders()
        except Exception as e:
            print(f"Scheduler error: {e}")
        time.sleep(60)  # check every 60 seconds

@app.on_event("startup")
def start_scheduler():
    thread = threading.Thread(target=reminder_scheduler, daemon=True)
    thread.start()
    print("🚀 App started with email reminders running in background!")
