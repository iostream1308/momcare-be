import email
import imp
from lib2to3.pgen2 import token
from random import random
from telnetlib import STATUS

from fastapi import Depends, FastAPI, Query, Body, status, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Set
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session


from momcare import crud, models, schemas
from momcare.database import SessionLocal, engine 



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
def show():
    return "hello"

@app.post("/usercreate/", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db, user)

@app.get("/user/{email}")
def read_user(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@app.get("/user/role/{role}")
def user_by_role(role: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_role(db, role)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@app.post("/change_pass/", status_code=status.HTTP_201_CREATED)
def update(email: str, new_pass: str, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email) is None:
        raise HTTPException(status_code=404, detail="user not found")
        return None
    user_update = crud.update_user(db, email, new_pass)
    return user_update