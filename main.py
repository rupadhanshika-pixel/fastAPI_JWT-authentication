# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt
# from datetime import datetime, timedelta

# app = FastAPI()

# SECRET_KEY = "mysecretkey"
# ALGORITHM = "HS256"

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# # Create JWT Token
# def create_token(data: dict):
#     expire = datetime.utcnow() + timedelta(minutes=30)
#     data.update({"exp": expire})
#     token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
#     return token


# # Login API
# @app.post("/login")
# def login():
#     token = create_token({"username": "rupa"})
#     return {"access_token": token}


# # Protected API
# @app.get("/profile")
# def profile(token: str = Depends(oauth2_scheme)):
#     return {"message": "You accessed protected route"}   

##JWT Authentication

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models, schemas
from database import engine, SessionLocal
from auth import create_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Register user
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}


# Login
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_token({"username": db_user.username})

    return {"access_token": token}