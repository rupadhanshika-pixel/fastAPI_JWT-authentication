from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=30)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)