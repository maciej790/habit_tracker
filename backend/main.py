#from typing import Union
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlmodel import Session, select
from routers import user
from database import create_db_and_tables, get_session
from models.habit import Habit, HabitLog
from models.user import User
from routers import habit

app = FastAPI()

app.include_router(user.router)
app.include_router(habit.router)

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

#setup db tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

