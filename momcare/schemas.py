from enum import Enum
from typing import List
from pydantic import BaseModel
from datetime import datetime, date

from .models import Role, Sex, ConvState, MessState, AppoState, Service, InvoiceStatus, PaymentStatus, PaymentMethod

class DoctorUpdate(BaseModel):
    creatorRole: Role
    creatorId: int
    name: str = None
    age: int = None
    sex: Sex = None
    phone: str = None
    medicalSpecialtyId: int = None
    hospitalId: int = None
    degree: str = None
    consultingPriceViaMessage: float = None
    consultingPriceViaCall: float = None
    point: float = None

class UserBase(BaseModel):
    email: str
    role: Role

class UserCreate(UserBase):
    password: str

class User(UserBase):
    # userId: int
    password_hash: str
    

    class Config:
        orm_mode = True
        
class Patient(BaseModel):
    email: str
    password: str
    name: str
    age: int
    sex: Sex
    phone: str
    address: str

    class Config:
        orm_mode = True
        
class Hospital(BaseModel):
    # hospitalId: int
    # userId: int
    email: str
    password: str
    name: str
    address: str
    workingTime: str
    # point: float

    class Config:
        orm_mode = True
        
class MedicalSpecialty(BaseModel):
    # medicalSpecialtyid: int
    creatorRole: Role 
    englishName: str
    vietnameseName: str

    class Config:
        orm_mode = True
        
class Doctor(BaseModel):
    # doctorid: int 
    # userid: int
    creatorRole: Role
    creatorId: int
    email: str
    password: str
    name: str
    age: int
    sex: Sex
    phone: str
    medicalSpecialtyId: int
    hospitalId: int
    degree: str
    consultingPriceViaMessage: float
    consultingPriceViaCall: float
    # point: float

    class Config:
        orm_mode = True
        
class DoctorComment(BaseModel):
    # doctorCommentId: int
    # time: datetime
    patientId: int
    doctorId: int
    comment: str
    # point: float

    class Config:
        orm_mode = True
        
class HospitalCommentBase(BaseModel):
    # hospitalCommentId: int
    # time: datetime
    patientId: int
    hospitalId: int
    comment: str
    # point: float

    class Config:
        orm_mode = True
        
class Attachment(BaseModel):
    conversationId: int
    sender: int
    file: str

    class Config:
        orm_mode = True        

class Conversation(BaseModel):
    patientId: int
    doctorId: int
    startTime: datetime
    state: ConvState

    class Config:
        orm_mode = True

class Message(BaseModel):
    conversationId: int
    sender: int
    text: str

    class Config:
        orm_mode = True


class Call(BaseModel):
    callAppointmentId: int
    problems: str
    startTime: datetime
    endTime: datetime
    link: str

    class Config:
        orm_mode = True

class CallAppointment(BaseModel):
    # callAppointmentId: int
    time: datetime
    form: str
    doctorId: int
    patientId: int
    # state: AppoState
    # calls: List[Call] = []

    class Config:
        orm_mode = True   
        
class HospitalAppointment(BaseModel):
    # hospitalAppointmentId: int
    time: datetime
    hospitalId: int
    patientId: int
    # state: AppoState

    class Config:
        orm_mode = True

class MedicalHistory(BaseModel):
    patientId: int
    symptom: str
    existingDiseases: str

    class Config:
        orm_mode = True

class MedicalRecord(BaseModel):
    patientId: int
    doctorId: int
    time: datetime
    medicalHistoryId: int
    diagnostic: str
    note: str

    class Config:
        orm_mode = True

class Prescription(BaseModel):
    medicalRecordId: int
    medicinesNameAndDosages: str
    usageTime: str
    note: str
    
    class Config:
        orm_mode = True     

class Invoice(BaseModel):
    consultingServices: Service
    callAppointmentId: int
    conversationId: int
    time: datetime
    dueTime: datetime
    totalAmount: float
    note: str
    status: InvoiceStatus

    class Config:
        orm_mode = True

class Payment(BaseModel):
    patientId: int
    amount: float
    paymentTime: datetime
    status: PaymentStatus
    paymentMethod: PaymentMethod

    class Config:
        orm_mode = True

class Transaction(BaseModel):
    invoiceId: int
    paymentId: int
    time: datetime
    amount: float
    description: str

    class Config:
        orm_mode = True