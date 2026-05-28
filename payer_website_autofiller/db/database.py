"""Database module"""

# pylint: disable=invalid-name

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

HOST = "db"
PORT = 3306

DATEBASE_URL = (
    f"mysql+pymysql://{os.getenv("MYSQL_USER")}"
    f":{os.getenv("MYSQL_PASSWORD")}"
    f"@{HOST}:{PORT}"
    f"/{os.getenv("MYSQL_DATABASE")}"
)


# Connect Database
engine = create_engine(DATEBASE_URL)

# Create session factory
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)

Base = declarative_base()
