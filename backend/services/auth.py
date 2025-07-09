# services/auth_service.py
from fastapi import Depends
from sqlmodel import Session, select
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from models.user import User
from database import get_session

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(id: int, username: str):
    data = {"sub": username, "id": id}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def login_user(username: str, password: str, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
