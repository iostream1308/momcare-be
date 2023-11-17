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



def create_user(db: Session, user: schemas.UserCreate):
    googleId = ""
    if user.googleId is not None:
        googleId = user.googleId
    p = user.email + user.password
    hash_object = hashlib.sha256(p.encode())
    pHash = hash_object.hexdigest()
    db_user = models.User(email=user.email,
                          role=user.role, password_hash=pHash, googleId=user.googleId)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def change_password(db: Session, email: str, new_pass: str):
    p = email + new_pass 
    hash_object = hashlib.sha256(p.encode())
    new_p_hash = hash_object.hexdigest()
    db.query(models.User).filter(models.User.email == email).update({"password_hash": new_p_hash})
    db.commit()
    return "ok"

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_role(db: Session, role: int):
    return db.query(models.User).filter(models.User.role == role).all()

def make_call_appointment(db: Session, appointment: schemas.CallAppointment):
    db_appointment = models.CallAppointment(time=datetime.utcnow(), form=appointment.form,
                                            doctorId=appointment.doctorId,
                                            patientId=appointment.patientId,
                                            state=models.AppoState.UNCOMFIRM)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def make_hospital_appointment(db: Session, appointment: schemas.HospitalAppointment):
    db_appointment = models.HospitalAppointment(time=datetime.utcnow(),
                                                hospitalId=appointment.hospitalId,
                                                patientId=appointment.patientId,
                                                state=models.AppoState.UNCOMFIRM)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def change_state_call_appointment(db: Session, callAppointmentId: int, state: models.AppoState):
    db.query(models.CallAppointment).filter(models.CallAppointment.callAppointmentId == callAppointmentId).update({
        "state": state
    })
    db.commit()
    return "ok"

def change_state_hospital_appointment(db: Session, hospitalAppointmentId: int, state: models.AppoState):
    db.query(models.HospitalAppointment).filter(models.HospitalAppointment.hospitalAppointmentId == hospitalAppointmentId).update({
        "state": state
    })
    db.commit()
    return "ok"

def add_doctor_comment(db: Session, comment: schemas.DoctorComment):
    db_comment = models.DoctorComment(time=datetime.utcnow(), patientId=comment.patientId,
                                      doctorId=comment.doctorId,
                                      comment=comment.comment)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def add_hospital_comment(db: Session, comment: schemas.HospitalCommentBase):
    db_comment = models.DoctorComment(time=datetime.utcnow(), patientId=comment.patientId,
                                      hospitalId=comment.hospitalId,
                                      comment=comment.comment)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment