from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import sessionmaker
import faker
import random
import hashlib
from datetime import datetime

random.seed(10)

fake = faker.Faker()
fake.seed_instance(4321)



###########################################################################################
engine = create_engine("mysql+mysqlconnector://abc:password@localhost:3306/momcare")
###########################################################################################



metadata = MetaData()
HospitalAppointment = Table('HospitalAppointment', metadata, autoload_with=engine)
CallAppointment = Table('CallAppointment', metadata, autoload_with=engine)

# User = Table('User', metadata, autoload_with=engine)
# Patient = Table('Patient', metadata, autoload_with=engine)
# Hospital = Table('Hospital', metadata, autoload_with=engine)
# Doctor = Table('Doctor', metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()

# number_patient = 200
# number_hospital = 10
# number_doctor = 200

# sex = ['MALE', 'FEMALE', 'NOT_MENTION']
# for i in range(1, number_patient):
#     name = fake.name()

#     email = name.replace(" ", "").lower() + str(random.randint(11, 11111)) + "@gmail.com"
#     p = email + "123456789"
#     hash_object = hashlib.sha256(p.encode())
#     pHash = hash_object.hexdigest()
#     session.execute(User.insert().values({
#         'userId': i,
#         'email': email,
#         'password_hash': pHash,
#         # password: 123456789
#         'role': 'PATIENT'
#     }))
#     session.execute(Patient.insert().values({
#         'userId': i,
#         'name': fake.name(),
#         'age': random.randint(7, 90),
#         'sex': sex[random.randint(0, len(sex) - 1)],
#         'phone': '0' + fake.msisdn()[:9],
#         'address': fake.address()
#     }))

# for i in range(number_patient, number_patient + number_hospital):
#     name = fake.name()

#     email = name.replace(" ", "").lower() + str(random.randint(11, 11111)) + "@gmail.com"
#     p = email + "123456789"
#     hash_object = hashlib.sha256(p.encode())
#     pHash = hash_object.hexdigest()
#     session.execute(User.insert().values({
#         'userId': i,
#         'email': email,
#         'password_hash': pHash,
#         'role': 'HOSPITAL'
#     }))
#     session.execute(Hospital.insert().values({
#         'userId': i,
#         'name': fake.city() + " Hospital",
#         'address': fake.address(),
#         'workingTime': 'Monday to Saturday from 8:00 AM to 5:00 PM',
#         'point': round(random.uniform(1.5, 4.9), 1)
#     }))

# degree = ['Associate Professors Doctor', 'Master', 'PhD', 'Bachelor']
# for i in range(number_patient + number_hospital, number_patient + number_hospital + number_doctor):
#     name = fake.name()

#     email = name.replace(" ", "").lower() + str(random.randint(11, 11111)) + "@gmail.com"
#     p = email + "123456789"
#     hash_object = hashlib.sha256(p.encode())
#     pHash = hash_object.hexdigest()
#     session.execute(User.insert().values({
#         'userId': i,
#         'email': email,
#         'password_hash': pHash,
#         'role': 'DOCTOR'
#     }))
#     consultingPriceViaMessage = random.randint(14, 19) + 0.99
#     session.execute(Doctor.insert().values({
#         'userId': i,
#         'name': fake.name(),
#         'age': random.randint(30, 53),
#         'sex': sex[random.randint(0, len(sex) - 1)],
#         'phone': '0' + fake.msisdn()[:9],
#         'medicalSpecialtyId': random.randint(1, 20),
#         'hospitalId': random.randint(1, number_hospital),
#         'degree': degree[random.randint(0, len(degree) - 1)],
#         'consultingPriceViaMessage': consultingPriceViaMessage,
#         'consultingPriceViaCall': consultingPriceViaMessage + 13,
#         'point': round(random.uniform(1.5, 4.9), 1)
#     }))

# for i in range(1, 100):
#     session.execute(HospitalAppointment.insert().values({
#         'hospitalAppointmentId': i,
#         'time': fake.date_time(),
#         'hospitalId': random.randint(1, 10),
#         'patientId': random.randint(1, 199),
#         'state': 'COMPLETED'
#     }))

##############################################################################

for i in range(1, 100):
    session.execute(HospitalAppointment.insert().values({
        'hospitalAppointmentId': i,
        'time': fake.date_time_between(start_date=datetime.strptime("2023-10-01", "%Y-%m-%d"),
                                       end_date=datetime.strptime("2023-12-30", "%Y-%m-%d")),
        'hospitalId': random.randint(1, 10),
        'patientId': random.randint(1, 199),
        'state': 'COMPLETED'
    }))

sset = set()
for i in range(100, 200):
    hospitalId = random.randint(1, 10)
    patientId = random.randint(1, 199)
    if (hospitalId, patientId) in sset:
        continue
    sset.add((hospitalId, patientId))
    
    session.execute(HospitalAppointment.insert().values({
        'hospitalAppointmentId': i,
        'time': fake.date_time_between(start_date=datetime.strptime("2024-01-01", "%Y-%m-%d"),
                                       end_date=datetime.strptime("2024-02-01", "%Y-%m-%d")),
        'hospitalId': hospitalId,
        'patientId': patientId,
        'state': 'CONFIRM'
    }))

for i in range(200, 300):
    hospitalId = random.randint(1, 10)
    patientId = random.randint(1, 199)
    if (hospitalId, patientId) in sset:
        continue
    sset.add((hospitalId, patientId))
    
    session.execute(HospitalAppointment.insert().values({
        'hospitalAppointmentId': i,
        'time': fake.date_time_between(start_date=datetime.strptime("2024-01-01", "%Y-%m-%d"),
                                       end_date=datetime.strptime("2024-02-01", "%Y-%m-%d")),
        'hospitalId': hospitalId,
        'patientId': patientId,
        'state': 'UNCOMFIRM'
    }))

######################

for i in range(1, 100):
    session.execute(CallAppointment.insert().values({
        'callAppointmentId': i,
        'time': fake.date_time_between(start_date=datetime.strptime("2023-10-01", "%Y-%m-%d"),
                                       end_date=datetime.strptime("2023-12-30", "%Y-%m-%d")),
        'doctorId': random.randint(1, 200),
        'patientId': random.randint(1, 199),
        'state': 'COMPLETED'
    }))

s = set()
for i in range(100, 200):
    doctorId = random.randint(1, 200)
    patientId = random.randint(1, 199)
    if (doctorId, patientId) in s:
        continue
    s.add((doctorId, patientId))
    
    session.execute(CallAppointment.insert().values({
        'callAppointmentId': i,
        'time': fake.date_time_between(start_date=datetime.strptime("2024-01-01", "%Y-%m-%d"),
                                       end_date=datetime.strptime("2024-02-01", "%Y-%m-%d")),
        'doctorId': doctorId,
        'patientId': patientId,
        'state': 'CONFIRM'
    }))

for i in range(200, 300):
    doctorId = random.randint(1, 200)
    patientId = random.randint(1, 199)
    if (doctorId, patientId) in s:
        continue
    s.add((doctorId, patientId))
    
    session.execute(CallAppointment.insert().values({
        'callAppointmentId': i,
        'time': fake.date_time_between(start_date=datetime.strptime("2024-01-01", "%Y-%m-%d"),
                                       end_date=datetime.strptime("2024-02-01", "%Y-%m-%d")),
        'doctorId': doctorId,
        'patientId': patientId,
        'state': 'UNCOMFIRM'
    }))

session.commit()
session.close()