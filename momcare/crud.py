import hashlib
import imp
from lib2to3.pgen2.token import OP
from statistics import mode
from time import time
from sqlalchemy import Interval, and_, asc, false, or_, not_, desc, asc, func, true
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy.orm import Session
# import bcrypt
# import jwt
from googletrans import Translator, constants
from pprint import pprint


from . import models, schemas
from .models import Role

def check_registered_user(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        return "not registered"
    return "registered"

def create_user(db: Session, email: str, password: str, role: Role):
    p = email + password
    hash_object = hashlib.sha256(p.encode())
    pHash = hash_object.hexdigest()
    db_user = models.User(email=email,
                          role=role, password_hash=pHash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_patient(db: Session, patient: schemas.Patient):
    if check_registered_user(db, patient.email) == "registered":
        return "email already exists"
    user: models.User = create_user(db, patient.email, patient.password, Role.PATIENT)
    print()
    db_patient = models.Patient(userId = user.userId, name = patient.name,
                                age = patient.age, sex = patient.sex, phone = patient.phone,
                                address = patient.address)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def create_hospital(db: Session, hospital: schemas.Hospital):
    if check_registered_user(db, hospital.email) == "registered":
        return "email already exists"
    user: models.User = create_user(db, hospital.email, hospital.password, Role.HOSPITAL)
    db_hospital = models.Hospital(userId = user.userId, name = hospital.name,
                                address = hospital.address, workingTime = hospital.workingTime)
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def get_list_hospital(db: Session):
    return db.query(models.Hospital).all()

def get_hospital_by_id(db: Session, id: int):
    return db.query(models.Hospital).filter(models.Hospital.hospitalId == id).first()

def check_registered_medical_specialty(db: Session, medSpec: schemas.MedicalSpecialty):
    ms = db.query(models.MedicalSpecialty).filter(and_(models.MedicalSpecialty.englishName == medSpec.englishName, 
                                                         models.MedicalSpecialty.vietnameseName == medSpec.vietnameseName)).first()
    if ms is None:
        return "not registered"
    return "registered"

def check_login(db: Session, email: str, password: str):
    if check_registered_user(db, email) == "not registered":
        return "not registered"
    user: models.User = db.query(models.User).filter(models.User.email == email).first()
    p = email + password
    hash_object = hashlib.sha256(p.encode())
    pHash = hash_object.hexdigest()
    if user.password_hash != pHash:
        return "wrong password"
    return user.role

def create_medicalSpecialty(db: Session, medSpec: schemas.MedicalSpecialty, ):
    if check_registered_medical_specialty(db, medSpec) == "registered":
        return "already exists"
    db_medspec = models.MedicalSpecialty(englishName = medSpec.englishName, vietnameseName = medSpec.vietnameseName)
    db.add(db_medspec)
    db.commit()
    db.refresh(db_medspec)
    return db_medspec

def request_create_medicalSpeciality(db: Session, medSpec: schemas.MedicalSpecialty):
    if medSpec.creatorRole == Role.PATIENT or medSpec.creatorRole == Role.DOCTOR:
        return "not permission"
    return create_medicalSpecialty(db, medSpec)

def get_list_medicalSpecialty(db: Session):
    return db.query(models.MedicalSpecialty).all()

def get_medicalSpecialty_by_id(db: Session, id: int):
    return db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.medicalSpecialtyId == id).first()

def get_medicalSpecialty_by_vi(db: Session, vi: int):
    return db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.vietnameseName == vi).first()

def get_medicalSpecialty_by_en(db: Session, en: int):
    return db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.englishName == en).first()

def create_doctor(db: Session, doctor: schemas.Doctor):
    if check_registered_user(db, doctor.email) == "registered":
        return "email already exists"
    user: models.User = create_user(db, doctor.email, doctor.password, Role.DOCTOR)
    db_doctor = models.Doctor(userId = user.userId, name = doctor.name, age = doctor.age,
                               sex = doctor.sex, phone = doctor.phone, 
                               medicalSpecialtyId = doctor.medicalSpecialtyId,
                               hospitalId = doctor.hospitalId, degree = doctor.degree,
                               consultingPriceViaMessage = doctor.consultingPriceViaMessage,
                               consultingPriceViaCall = doctor.consultingPriceViaCall)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor
    
    
def request_register_doctor(db: Session, doctor: schemas.Doctor):
    if doctor.creatorRole == Role.PATIENT or doctor.creatorRole == Role.DOCTOR:
        return "not permission"
    if get_hospital_by_id(db, doctor.hospitalId) == None:
        return "hospital not exists"
    if get_medicalSpecialty_by_id(db, doctor.medicalSpecialtyId) == None:
        return "medical specialty not exists"
    if doctor.creatorId != doctor.hospitalId:
        return "different hospital"
    return create_doctor(db, doctor)

def get_list_doctor(db: Session):
    return db.query(models.Doctor).all()

def get_doctor_by_id(db: Session, id: int):
    return db.query(models.Doctor).filter(models.Doctor.doctorId == id).first()

def get_list_doctors_of_hospital(db: Session, hospitalid: int):
    return db.query(models.Doctor).filter(models.Doctor.hospitalId == hospitalid).all()
    
def change_password(db: Session, email: str, new_pass: str):
    if check_registered_user(db, email) == "not registered":
        return "not registered"
    p = email + new_pass 
    hash_object = hashlib.sha256(p.encode())
    new_p_hash = hash_object.hexdigest()
    db.query(models.User).filter(models.User.email == email).update({"password_hash": new_p_hash})
    db.commit()
    return "ok"

def get_user_by_email(db: Session, email: str):
    if check_registered_user(db, email) == "not registered":
        return "not registered"
    return db.query(models.User).filter(models.User.email == email).first()

