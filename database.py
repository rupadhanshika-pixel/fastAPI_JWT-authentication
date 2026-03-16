# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "sqlite:///./users.db"

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal = sessionmaker(bind=engine)

# Base = declarative_base() 

##postgre sql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:20102015@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()