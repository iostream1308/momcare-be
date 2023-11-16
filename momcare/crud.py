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
