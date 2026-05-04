from sqlmodel import create_engine,Session
from fastapi import Depends
from typing import Annotated
from sqlalchemy import URL


DB_URL = URL.create(
    drivername="mysql+mysqldb",
    username="root",
    password="admin",
    host="localhost",
    port=3306,
    database="ecommerce"
)
# args = {"check_same_thread": False}
engine = create_engine(DB_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]
