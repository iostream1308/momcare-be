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

@app.get("/check/")
def get_current_user(token: str, db: Session = Depends(get_db)):
    # credentials_exception = HTTPException(
    #     status_code=401,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    return crud.verify_token(db, token)

@app.post("/create_patient/")
def create_patient(patient: schemas.Patient, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@app.post("/create_hospital/")
def create_hospital(hospital: schemas.Hospital, db: Session = Depends(get_db)):
    return crud.create_hospital(db, hospital)

@app.post("/create_medspec/")
def create_medspec(medspec: schemas.MedicalSpecialty, db: Session = Depends(get_db)):
    return crud.request_create_medicalSpeciality(db, medspec)

@app.post("/create_doctor/")
def create_doctor(doctor: schemas.Doctor, db: Session = Depends(get_db)):
    return crud.request_register_doctor(db, doctor)

@app.post("/change_pass/")
def change_pass(email: str, new_pass: str, db: Session = Depends(get_db)):
    return crud.change_password(db, email, new_pass)

@app.get("/hospital/")
def hospitals(db: Session = Depends(get_db)):
    return crud.get_list_hospital(db)

@app.get("/hospital/name/")
def hospitals_by_name(name: str, db: Session = Depends(get_db)):
    return crud.get_list_hospitals_by_name(db, name)

@app.get("/hospital/{id}")
def hospitals(id: int, db: Session = Depends(get_db)):
    return crud.get_hospital_by_id(db, id)

@app.get("/login/")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return crud.login(db, email, password)

@app.get("/logout")
def logout(token: str):
    return crud.logout(token)

@app.get("/medspec/")
def medicalSpecialty(db: Session = Depends(get_db)):
    return crud.get_list_medicalSpecialty(db)

@app.get("/medspec/{id}")
def medicalSpecialty_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_medicalSpecialty_by_id(db, id)

@app.get("/medspec/vi/{vi}")
def medicalSpecialty_by_vi(vi: str, db: Session = Depends(get_db)):
    return crud.get_medicalSpecialty_by_vi(db, vi)

@app.get("/medspec/en/{en}")
def medicalSpecialty_by_en(en: str, db: Session = Depends(get_db)):
    return crud.get_medicalSpecialty_by_en(db, en)

@app.get("/doctor/")
def doctor(db: Session = Depends(get_db)):
    return crud.get_list_doctor(db)

@app.get("/doctor/name/")
def doctors_by_name(name: str, db: Session = Depends(get_db)):
    return crud.get_list_doctors_by_name(db, name)

@app.get("/doctor/{id}")
def doctor_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_doctor_by_id(db, id)

@app.get("/doctor/hospital/{id}")
def doctor_by_hospitalid(id: int, db: Session = Depends(get_db)):
    return crud.get_list_doctors_of_hospital(db, id)

@app.get("/user/{email}")
def user_by_email(email: str, db: Session = Depends(get_db)):
    return crud.get_user_by_email(db, email)

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