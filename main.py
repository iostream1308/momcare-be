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

@app.get("/hospital/{id}")
def hospitals(id: int, db: Session = Depends(get_db)):
    return crud.get_hospital_by_id(db, id)

@app.get("/login/")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return crud.check_login(db, email, password)

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

@app.get("/doctor/{id}")
def doctor_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_doctor_by_id(db, id)

@app.get("/doctor/hospital/{id}")
def doctor_by_hospitalid(id: int, db: Session = Depends(get_db)):
    return crud.get_list_doctors_of_hospital(db, id)

@app.get("/user/{email}")
def user_by_email(email: str, db: Session = Depends(get_db)):
    return crud.get_user_by_email(db, email)
