import hashlib
import imp
import json
from lib2to3.pgen2.token import OP
from statistics import mode
from time import time
from sqlalchemy import Interval, and_, asc, false, or_, not_, desc, asc, func, true
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pathlib import Path
import jwt
from googletrans import Translator, constants
from pprint import pprint

from . import models, schemas
from .models import Role

from momcare.models import *
import pytz


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
    db_patient = models.Patient(userId=user.userId, name=patient.name,
                                age=patient.age, sex=patient.sex, phone=patient.phone,
                                address=patient.address)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def create_hospital(db: Session, hospital: schemas.Hospital):
    if check_registered_user(db, hospital.email) == "registered":
        return "email already exists"
    user: models.User = create_user(db, hospital.email, hospital.password, Role.HOSPITAL)
    db_hospital = models.Hospital(userId=user.userId, name=hospital.name,
                                  address=hospital.address, workingTime=hospital.workingTime)
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital


def get_list_hospital(db: Session):
    return db.query(models.Hospital).all()


def get_list_hospitals_by_name(db: Session, name: str):
    return db.query(models.Hospital).filter(models.Hospital.name.like(f"%{name}%")).all()


def get_hospital_by_id(db: Session, id: int):
    return db.query(models.Hospital).filter(models.Hospital.hospitalId == id).first()


def check_registered_medical_specialty(db: Session, medSpec: schemas.MedicalSpecialty):
    ms = db.query(models.MedicalSpecialty).filter(and_(models.MedicalSpecialty.englishName == medSpec.englishName,
                                                       models.MedicalSpecialty.vietnameseName == medSpec.vietnameseName)).first()
    if ms is None:
        return "not registered"
    return "registered"


def create_medicalSpecialty(db: Session, medSpec: schemas.MedicalSpecialty, ):
    if check_registered_medical_specialty(db, medSpec) == "registered":
        return "already exists"
    db_medspec = models.MedicalSpecialty(englishName=medSpec.englishName, vietnameseName=medSpec.vietnameseName)
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
    return db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.vietnameseName.like(f"%{vi}%")).first()


def get_medicalSpecialty_by_en(db: Session, en: int):
    return db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.vietnameseName.like(f"%{en}%")).first()


def create_doctor(db: Session, doctor: schemas.Doctor):
    if check_registered_user(db, doctor.email) == "registered":
        return "email already exists"
    user: models.User = create_user(db, doctor.email, doctor.password, Role.DOCTOR)
    db_doctor = models.Doctor(userId=user.userId, name=doctor.name, age=doctor.age,
                              sex=doctor.sex, phone=doctor.phone,
                              medicalSpecialtyId=doctor.medicalSpecialtyId,
                              hospitalId=doctor.hospitalId, degree=doctor.degree,
                              consultingPriceViaMessage=doctor.consultingPriceViaMessage,
                              consultingPriceViaCall=doctor.consultingPriceViaCall)
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


def get_list_doctors_by_name(db: Session, name: str):
    return db.query(models.Doctor).filter(models.Doctor.name.like(f"%{name}%")).all()


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


def get_user_by_role(db: Session, role: int):
    return db.query(models.User).filter(models.User.role == role).all()


def check_permission(db: Session, user_id: int, role: Role):
    return db.query(User).filter(User.userId == user_id).first().role == role


# Appointment

def make_call_appointment(db: Session, appointment: schemas.CallAppointment):
    if appointment.time <= datetime.utcnow().replace(tzinfo=pytz.utc):
        return "cannot choose a time in the past"

    appointments = db.query(CallAppointment).filter(
        CallAppointment.doctorId == appointment.doctorId).order_by(getattr(CallAppointment, "time")).all()
    for app in appointments:
        if (appointment.time <= (app.time + timedelta(hours=1)).replace(tzinfo=pytz.utc)) and (
                appointment.time + timedelta(hours=1) >= app.time.replace(tzinfo=pytz.utc)):
            return "doctor is busy"

    appointments = db.query(CallAppointment).filter(
        CallAppointment.patientId == appointment.patientId).order_by(getattr(CallAppointment, "time")).all()
    for app in appointments:
        if (appointment.time <= (app.time + timedelta(hours=1)).replace(tzinfo=pytz.utc)) and (
                appointment.time + timedelta(hours=1) >= app.time.replace(tzinfo=pytz.utc)):
            return "patient is busy"

    db_appointment = models.CallAppointment(time=appointment.time, form=appointment.form,
                                            doctorId=appointment.doctorId,
                                            patientId=appointment.patientId,
                                            state=models.AppoState.UNCOMFIRM)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def make_hospital_appointment(db: Session, appointment: schemas.HospitalAppointment):
    db_appointment = models.HospitalAppointment(time=appointment.time,
                                                hospitalId=appointment.hospitalId,
                                                patientId=appointment.patientId,
                                                state=models.AppoState.UNCOMFIRM)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def change_time_call_appointment(db: Session, user_id: int, callAppointmentId: int, time: datetime):
    if not check_permission(db, user_id, Role.DOCTOR):
        return "not permission"
    db.query(models.CallAppointment).filter(models.CallAppointment.callAppointmentId == callAppointmentId).update({
        "time": time
    })
    db.commit()
    return "ok"


def change_time_hospital_appointment(db: Session, user_id: int, hospitalAppointmentId: int, time: datetime):
    if not check_permission(db, user_id, Role.HOSPITAL):
        return "not permission"
    db.query(models.HospitalAppointment).filter(
        models.HospitalAppointment.hospitalAppointmentId == hospitalAppointmentId).update({
        "time": time
    })
    db.commit()
    return "ok"


def change_state_hospital_appointment(db: Session, user_id: int, hospitalAppointmentId: int, state: models.AppoState):
    if not check_permission(db, user_id, Role.HOSPITAL):
        return "not permission"
    db.query(models.HospitalAppointment).filter(
        models.HospitalAppointment.hospitalAppointmentId == hospitalAppointmentId).update({
        "state": state
    })
    db.commit()
    return "ok"


def change_state_call_appointment(db: Session, user_id: int, callAppointmentId: int, state: models.AppoState):
    if not check_permission(db, user_id, Role.DOCTOR):
        return "not permission"
    db.query(models.CallAppointment).filter(models.CallAppointment.callAppointmentId == callAppointmentId).update({
        "state": state
    })
    db.commit()
    return "ok"


def get_appointments_of_user(db: Session, user_id: int):
    user = db.query(User).filter(User.userId == user_id).first()
    if user.role == Role.PATIENT:
        return db.query(CallAppointment).filter(CallAppointment.patientId
                                                == db.query(Patient).filter(Patient.userId == user_id).first().patientId
                                                ).order_by(getattr(CallAppointment, "time")).all()
    elif user.role == Role.DOCTOR:
        return db.query(CallAppointment).filter(CallAppointment.doctorId
                                                == db.query(Doctor).filter(Doctor.userId == user_id).first().doctorId
                                                ).order_by(getattr(CallAppointment, "time")).all()
    elif user.role == Role.HOSPITAL:
        return db.query(HospitalAppointment).filter(HospitalAppointment.hospitalId
                                                    == db.query(Hospital).filter(
            Hospital.userId == user_id).first().hospitalId
                                                    ).order_by(getattr(HospitalAppointment, "time")).all()


# Comment

def add_doctor_comment(db: Session, comment: schemas.DoctorComment):
    db_comment = models.DoctorComment(time=datetime.utcnow(), patientId=comment.patientId,
                                      doctorId=comment.doctorId,
                                      comment=comment.comment,
                                      point=comment.point)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def add_hospital_comment(db: Session, comment: schemas.HospitalCommentBase):
    db_comment = models.HospitalComment(time=datetime.utcnow(), patientId=comment.patientId,
                                        hospitalId=comment.hospitalId,
                                        comment=comment.comment,
                                        point=comment.point)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_doctor_comments_by_doctor_id(db: Session, doctor_id: int):
    res = []
    comments = db.query(DoctorComment).filter(DoctorComment.doctorId == doctor_id).all()
    for comment in comments:
        res.append([comment, db.query(Patient).filter(Patient.patientId == comment.patientId).first()])
    return res[::-1]


def get_hospital_comments_by_hospital_id(db: Session, hospital_id: int):
    res = []
    comments = db.query(HospitalComment).filter(HospitalComment.hospitalId == hospital_id).all()
    for comment in comments:
        res.append([comment, db.query(Patient).filter(Patient.patientId == comment.patientId).first()])
    return res[::-1]

# Function to create a new token
def create_token(db: Session, user_id: int, expires: bool):
    delta = timedelta(minutes=15)  # Token expires in 15 minutes
    if expires:
        expiration = datetime.utcnow() + delta
    else:
        expiration = None
    print(expiration)
    payload = {"user_id": user_id, "expires": expires, "exp": expiration.timestamp()}
    print(payload)
    # use user_id as secret key
    token = jwt.encode(payload, str(user_id), algorithm="HS256")
    db_token = models.Token(userId=user_id, token=token, expires=expires)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def login(db: Session, email: str, password: str):
    if check_registered_user(db, email) == "not registered":
        return "not registered"
    user: models.User = db.query(models.User).filter(models.User.email == email).first()
    p = email + password
    hash_object = hashlib.sha256(p.encode())
    pHash = hash_object.hexdigest()
    if user.password_hash != pHash:
        return "wrong password"
    token: models.Token = create_token(db, user.userId, False)
    # return object contains token and user
    return {"token": token.token, "user": { "id": user.userId, "role": user.role }}


# Function to verify and return the current user from the token
def verify_token(token: str, user_id: str):
    try:
        payload = jwt.decode(token, str(user_id), algorithms=["HS256"])
        expiration_time = payload['exp']  # Lấy thời gian hết hạn từ payload
        current_time = datetime.utcnow().timestamp()
        if expiration_time < current_time:
            return "ExpiredSignatureError"
    except jwt.ExpiredSignatureError:
        return "ExpiredSignatureError"
    except jwt.InvalidTokenError:
        return "InvalidTokenError"
    return "ok"


def get_current_user(db: Session, token: str):
    token_db: models.Token = db.query(models.Token).filter(models.Token.token == token).first()
    if token_db == None:
        return "token not exists"
    verify = verify_token(token, token_db.userId)
    if verify != "ok":
        return verify
    return db.query(models.User).filter(models.User.userId == token_db.userId).first()


# Function to logout user and delete the token
def logout(db: Session, token: str):
    db.query(models.Token).filter(models.Token.token == token).delete()
    db.commit()
