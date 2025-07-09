from fastapi import FastAPI
from config.database import create_db_and_tables
from api.routers import user, habit

app = FastAPI()

app.include_router(user.router)
app.include_router(habit.router)

#setup db tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

