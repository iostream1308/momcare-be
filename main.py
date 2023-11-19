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
from datetime import datetime


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


# Appointment

@app.post("/make_call_appointment/")
def make_call_appointment(appointment: schemas.CallAppointment, db: Session = Depends(get_db)):
    return crud.make_call_appointment(db, appointment)

@app.post("/change_time_call_appointment/", status_code=status.HTTP_201_CREATED)
def change_time_call_appointment(user_id: int, callAppointmentId: int, time: datetime, db: Session = Depends(get_db)):
    return crud.change_time_call_appointment(db, user_id, callAppointmentId, time)

@app.post("/change_state_call_appointment/", status_code=status.HTTP_201_CREATED)
def change_state_call_appointment(user_id: int, callAppointmentId: int, state: models.AppoState, db: Session = Depends(get_db)):
    return crud.change_state_call_appointment(db, user_id, callAppointmentId, state)

@app.post("/make_hospital_appointment/", response_model=schemas.HospitalAppointment)
def make_hospital_appointment(appointment: schemas.HospitalAppointment, db: Session = Depends(get_db)):
    return crud.make_hospital_appointment(db, appointment)

@app.post("/change_time_hospital_appointment/", status_code=status.HTTP_201_CREATED)
def change_time_call_appointment(user_id: int, hospitalAppointmentId: int, time: datetime, db: Session = Depends(get_db)):
    return crud.change_time_hospital_appointment(db, user_id, hospitalAppointmentId, time)

@app.post("/change_state_hospital_appointment/", status_code=status.HTTP_201_CREATED)
def change_state_hospital_appointment(user_id: int, hospitalAppointmentId: int, state: models.AppoState, db: Session = Depends(get_db)):
    return crud.change_state_hospital_appointment(db, user_id, hospitalAppointmentId, state)

@app.get("/users/{user_id}/appointments/")
def get_appointments_of_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_appointments_of_user(db, user_id)


# Comment

@app.post("/add_doctor_comment/", response_model=schemas.DoctorComment)
def add_doctor_comment(comment: schemas.DoctorComment, db: Session = Depends(get_db)):
    return crud.add_doctor_comment(db, comment)

@app.post("/add_hospital_comment/", response_model=schemas.HospitalCommentBase)
def add_hospital_comment(comment: schemas.HospitalCommentBase, db: Session = Depends(get_db)):
    return crud.add_hospital_comment(db, comment)

@app.get("/doctors/{doctor_id}/comments/")
def get_doctor_comments_by_doctor_id(doctor_id: int, db: Session = Depends(get_db)):
    return crud.get_doctor_comments_by_doctor_id(db, doctor_id)

@app.get("/hospitals/{hospital_id}/comments/")
def get_doctor_comments_by_hospital_id(hospital_id: int, db: Session = Depends(get_db)):
    return crud.get_hospital_comments_by_hospital_id(db, hospital_id)