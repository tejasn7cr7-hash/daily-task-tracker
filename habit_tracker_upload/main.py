from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine
import models
from routers import habits, tasks

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit & Task Tracker")

app.include_router(habits.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
