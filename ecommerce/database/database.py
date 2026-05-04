from sqlmodel import create_engine,Session
from fastapi import Depends
from typing import Annotated
from sqlalchemy import URL
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_URL = URL.create(
    drivername="mysql+pymysql",
    username=getenv("DB_USERNAME"),
    password=getenv("DB_PASSWORD"),
    host=getenv("DB_HOST"),
    port=int(getenv("DB_PORT", 3306)),
    database=getenv("DATABASE")
)

engine = create_engine(DB_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]
