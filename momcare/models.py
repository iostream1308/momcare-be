import enum
from sqlalchemy import Boolean, Column, BigInteger, Enum, Float, Integer, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base


class Role(int, enum.Enum):
    ADMIN = 1
    PATIENT = 2
    DOCTOR = 3
    HOSPITAL = 4
    
class User(Base):
    __tablename__ = 'User'

    userId = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(Enum(Role), nullable=False)
    googleId = Column(String(128))

    # patient = relationship('Patient', back_populates='user')
    # doctor = relationship('Doctor', back_populates='user')
    

class Sex(str, enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    NOT_MENTION = 'not_mention'   


class Patient(Base):
    __tablename__ = 'Patient'

    patientId = Column(BigInteger, primary_key=True, index=True)
    userId = Column(BigInteger, ForeignKey('User.userId'))
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    sex = Column(Enum(Sex))
    phone = Column(String(20))
    address = Column(Text)

    # # Define the relationship with User
    # user = relationship('User', back_populates='patient')

    # # Define the relationship with CallAppointment
    # call_appointments = relationship('CallAppointment', back_populates='patient')

    # # Define the relationship with MedicalHistory
    # medical_history = relationship('MedicalHistory', back_populates='patient')

    # # Define the relationship with MedicalRecord
    # medical_records = relationship('MedicalRecord', back_populates='patient')

    # # Define the relationship with HospitalAppointment
    # hospital_appointments = relationship('HospitalAppointment', back_populates='patient')

    # # Define the relationship with HospitalComment
    # hospital_comments = relationship('HospitalComment', back_populates='patient')

    # # Define the relationship with DoctorComment
    # doctor_comments = relationship('DoctorComment', back_populates='patient')

    # conversations = relationship('Conversation', back_populates='patient')
    
    # payments = relationship('Payment', back_populates='patient')


class Hospital(Base):
    __tablename__ = 'Hospital'

    hospitalId = Column(BigInteger, primary_key=True, index=True)
    userId = Column(BigInteger, ForeignKey('User.userId'))
    name = Column(String(500), nullable=False)
    address = Column(Text)
    workingTime = Column(Text)
    point = Column(Float)
    
    # hospital_comments = relationship('HospitalComment', back_populates='hospital')

    # hospital_appointments = relationship('HospitalAppointment', back_populates='hospital')
    
class MedicalSpecialty(Base):
    __tablename__ = 'MedicalSpecialty'
    
    medicalSpecialtyId = Column(Integer, primary_key=True, index=True)
    englishName = Column(String(100))
    vietnameseName = Column(String(100))
    
    # doctors = relationship('Doctor', back_populates='medical_specialty')
    
class Doctor(Base):
    __tablename__ = 'Doctor'

    doctorId = Column(BigInteger, primary_key=True, index=True)
    userId = Column(BigInteger, ForeignKey('User.userId'))
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    sex = Column(Enum(Sex))
    phone = Column(String(20))
    medicalSpecialtyId = Column(Integer, ForeignKey('MedicalSpecialty.medicalSpecialtyId'))
    hospitalId = Column(Integer, ForeignKey('Hospital.hospitalID'))
    degree = Column(String(300))
    consultingPriceViaMessage = Column(Float, default=0)
    consultingPriceViaCall = Column(Float, default=0)
    point = Column(Float)

    # Define the relationship with User
    # user = relationship('User', back_populates='doctor')

    # # Define the relationship with MedicalSpecialty
    # medical_specialty = relationship('MedicalSpecialty', back_populates='doctors')

    # # Define the relationship with CallAppointment
    # call_appointments = relationship('CallAppointment', back_populates='doctor')

    # # Define the relationship with Conversation
    # conversations = relationship('Conversation', back_populates='doctor')

    # doctor_comments = relationship('DoctorComment', back_populates='doctor')
    
    # medical_records = relationship('MedicalRecord', back_populates='doctor')
    
    
class DoctorComment(Base):
    __tablename__ = 'DoctorComment'

    doctorCommentId = Column(BigInteger, primary_key=True, index=True)
    time = Column(DateTime)
    patientId = Column(BigInteger, ForeignKey('Patient.patientId'), nullable=False)
    doctorId = Column(BigInteger, ForeignKey('Doctor.doctorId'), nullable=False)
    comment = Column(Text)
    point = Column(Float)

    # Define the relationship with Patient
    # patient = relationship('Patient', back_populates='doctor_comments')

    # # Define the relationship with Doctor
    # doctor = relationship('Doctor', back_populates='doctor_comments')
    
    
class HospitalComment(Base):
    __tablename__ = 'HospitalComment'

    hospitalCommentId = Column(BigInteger, primary_key=True, index=True)
    time = Column(DateTime)
    patientId = Column(BigInteger, ForeignKey('Patient.patientId'), nullable=False)
    hospitalId = Column(BigInteger, ForeignKey('Hospital.hospitalId'), nullable=False)
    comment = Column(Text)
    point = Column(Float)

    # Define the relationship with Patient
    # patient = relationship('Patient', back_populates='hospital_comments')

    # # Define the relationship with Hospital
    # hospital = relationship('Hospital', back_populates='hospital_comments')
    
    
class ConvState(str, enum.Enum):
    CLOSED = 'closed'
    KEEP = 'keep'
    
class Conversation(Base):
    __tablename__ = 'Conversation'

    conversationId = Column(BigInteger, primary_key=True, index=True)
    patientId = Column(BigInteger, ForeignKey('Patient.patientId'), nullable=False)
    doctorId = Column(BigInteger, ForeignKey('Doctor.doctorId'), nullable=False)
    startTime = Column(DateTime)
    state = Column(Enum(ConvState))

    # Define the relationship with Patient
    # patient = relationship('Patient', back_populates='conversations')

    # # Define the relationship with Doctor
    # doctor = relationship('Doctor', back_populates='conversations')

    # # Define the relationship with Attachment
    # attachments = relationship('Attachment', back_populates='conversation')

    # messages = relationship('Message', back_populates='conversation')

    # invoice = relationship('Invoice', back_populates='conversation')
    
    
class MessState(str, enum.Enum):
    SEEN = 'seen'
    NOT_SEEN = 'not_seen'
    
    
class Message(Base):
    __tablename__ = 'Message'

    messageId = Column(BigInteger, primary_key=True, index=True)
    conversationId = Column(BigInteger, ForeignKey('Conversation.conversationId'), nullable=False)
    sender = Column(BigInteger, ForeignKey('User.userId'), nullable=False)
    text = Column(Text)
    time = Column(DateTime)
    state = Column(Enum(MessState))

    # Define the relationship with Conversation
    # conversation = relationship('Conversation', back_populates='messages')
    
    
class Attachment(Base):
    __tablename__ = 'Attachment'

    attachmentId = Column(BigInteger, primary_key=True, index=True)
    conversationId = Column(BigInteger, ForeignKey('Conversation.conversationId'), nullable=False)
    sender = Column(BigInteger, ForeignKey('User.userId'), nullable=False)
    file = Column(String(500))
    time = Column(DateTime)
    state = Column(Enum(MessState))

    # Define the relationship with Conversation
    # conversation = relationship('Conversation', back_populates='attachments')


class AppoState(str, enum.Enum):
    CONFIRM = 'confirm'
    UNCOMFIRM = 'unconfirm'
    COMPLETED = 'completed'
    
    
class CallAppointment(Base):
    __tablename__ = 'CallAppointment'

    callAppointmentId = Column(BigInteger, primary_key=True, index=True)
    time = Column(DateTime)
    form = Column(String(128))
    doctorId = Column(BigInteger, ForeignKey('Doctor.doctorId'), nullable=False)
    patientId = Column(BigInteger, ForeignKey('Patient.patientId'), nullable=False)
    state = Column(Enum(AppoState))

    # Define the relationship with Doctor
    # doctor = relationship('Doctor', back_populates='call_appointments')

    # # Define the relationship with Patient
    # patient = relationship('Patient', back_populates='call_appointments')

    # # Define the relationship with Call
    # calls = relationship('Call', back_populates='call_appointment')

    # invoice = relationship('Invoice', back_populates='call_appointment')
    

class Call(Base):
    __tablename__ = 'Call'

    callId = Column(BigInteger, primary_key=True, index=True)
    callAppointmentId = Column(BigInteger, ForeignKey('CallAppointment.callAppointmentId'), nullable=False)
    problems = Column(Text)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    link = Column(String(500))

    # Define the relationship with CallAppointment
    # call_appointment = relationship('CallAppointment', back_populates='calls')
    
    
class HospitalAppointment(Base):
    __tablename__ = 'HospitalAppointment'

    hospitalAppointmentId = Column(BigInteger, primary_key=True, index=True)
    time = Column(DateTime)
    hospitalId = Column(BigInteger, ForeignKey('Hospital.hospitalId'), nullable=False)
    patientId = Column(BigInteger, ForeignKey('Patient.patientId'), nullable=False)
    state = Column(Enum(AppoState))

    # Define the relationship with Hospital
    # hospital = relationship('Hospital', back_populates='hospital_appointments')

    # # Define the relationship with Patient
    # patient = relationship('Patient', back_populates='hospital_appointments')
    
    
    
class MedicalHistory(Base):
    __tablename__ = 'MedicalHistory'

    medicalHistoryId = Column(BigInteger, primary_key=True, index=True)
    patientId = Column(BigInteger, ForeignKey('Patient.patientId'), nullable=False)
    symptom = Column(Text)
    existingDiseases = Column(Text)

    # Define the relationship with Patient
    # patient = relationship('Patient', back_populates='medical_history')

    # medical_records = relationship('MedicalRecord', back_populates='medical_history')

    
    
class MedicalRecord(Base):
    __tablename__ = 'MedicalRecord'

    medicalRecordId = Column(BigInteger, primary_key=True, index=True)
    patientId = Column(BigInteger, ForeignKey('Patient.patientId'), nullable=False)
    doctorId = Column(BigInteger, ForeignKey('Doctor.doctorId'), nullable=False)
    time = Column(DateTime)
    medicalHistoryId = Column(BigInteger, ForeignKey('MedicalHistory.medicalHistoryId'), nullable=False)
    diagnostic = Column(Text)
    note = Column(Text)

    # Define the relationship with Patient
    # patient = relationship('Patient', back_populates='medical_records')

    # # Define the relationship with Doctor
    # doctor = relationship('Doctor', back_populates='medical_records')

    # # Define the relationship with MedicalHistory
    # medical_history = relationship('MedicalHistory', back_populates='medical_records')
    
    # prescription = relationship('Prescription', back_populates='medical_record')

    
class Prescription(Base):
    __tablename__ = 'Prescription'

    prescriptionId = Column(BigInteger, primary_key=True, index=True)
    medicalRecordId = Column(BigInteger, ForeignKey('MedicalRecord.medicalRecordId'), nullable=False)
    medicinesNameAndDosages = Column(Text)
    usageTime = Column(Text)
    note = Column(Text)

    # Define the relationship with MedicalRecord
    # medical_record = relationship('MedicalRecord', back_populates='prescription')
    

    
class Service(str, enum.Enum):
    MESSAGE = 'message'
    CALL = 'call'
    BOTH = 'both'
    
    
class InvoiceStatus(str, enum.Enum):
    PAID = 'paid'
    UNPAID = 'unpaid'
    PAST_DUE = 'past_due'
    
    
class Invoice(Base):
    __tablename__ = 'Invoice'

    invoiceId = Column(BigInteger, primary_key=True, index=True)
    consultingServices = Column(Enum(Service))
    callAppointmentId = Column(BigInteger, ForeignKey('CallAppointment.callAppointmentId'), nullable=True)
    conversationId = Column(BigInteger, ForeignKey('Conversation.conversationId'), nullable=True)
    time = Column(DateTime)
    dueTime = Column(DateTime)
    totalAmount = Column(Float)
    note = Column(Text)
    status = Column(Enum(InvoiceStatus))

    # # Define the relationship with CallAppointment
    # call_appointment = relationship('CallAppointment', back_populates='invoice')

    # # Define the relationship with Conversation
    # conversation = relationship('Conversation', back_populates='invoice')

    # transactions = relationship('Transaction', back_populates='invoice')
    
    
class PaymentStatus(str, enum.Enum):
    PAID = 'paid'
    FAILED = 'failed'
    
class PaymentMethod(str, enum.Enum):
    CASH = 'cash'
    BANKING = 'banking'
    
class Payment(Base):
    __tablename__ = 'Payment'

    paymentId = Column(BigInteger, primary_key=True, index=True)
    patientId = Column(BigInteger, ForeignKey('Patient.patientId'), nullable=False)
    amount = Column(Float)
    paymentTime = Column(DateTime)
    status = Column(Enum(PaymentStatus))
    paymentMethod = Column(Enum(PaymentMethod))

    # Define the relationship with Patient
    # patient = relationship('Patient', back_populates='payments')

    # transactions = relationship('Transaction', back_populates='payment')

    
    
class Transaction(Base):
    __tablename__ = 'Transaction'

    transactionId = Column(BigInteger, primary_key=True, index=True)
    invoiceId = Column(BigInteger, ForeignKey('Invoice.invoiceId'), nullable=False)
    paymentId = Column(BigInteger, ForeignKey('Payment.paymentId'), nullable=False)
    time = Column(DateTime)
    amount = Column(Float)
    description = Column(Text)

    # Define the relationship with Invoice and Payment
    # invoice = relationship('Invoice', back_populates='transactions')
    # payment = relationship('Payment', back_populates='transactions')
    

    
