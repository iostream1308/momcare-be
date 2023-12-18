from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import sessionmaker
import faker
import random
import hashlib

random.seed(10)

fake = faker.Faker()
fake.seed_instance(4321)



###########################################################################################
engine = create_engine("mysql+mysqlconnector://abc:password@localhost:3306/momcare")
###########################################################################################



metadata = MetaData()
User = Table('User', metadata, autoload_with=engine)
Patient = Table('Patient', metadata, autoload_with=engine)
Hospital = Table('Hospital', metadata, autoload_with=engine)
Doctor = Table('Doctor', metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()

number_patient = 200
number_hospital = 10
number_doctor = 200

sex = ['MALE', 'FEMALE', 'NOT_MENTION']
for i in range(1, number_patient):
    name = fake.name()

    email = name.replace(" ", "").lower() + str(random.randint(11, 11111)) + "@gmail.com"
    p = email + "123456789"
    hash_object = hashlib.sha256(p.encode())
    pHash = hash_object.hexdigest()
    session.execute(User.insert().values({
        'userId': i,
        'email': email,
        'password_hash': pHash,
        # password: 123456789
        'role': 'PATIENT'
    }))
    session.execute(Patient.insert().values({
        'userId': i,
        'name': fake.name(),
        'age': random.randint(7, 90),
        'sex': sex[random.randint(0, len(sex) - 1)],
        'phone': '0' + fake.msisdn()[:9],
        'address': fake.address()
    }))

for i in range(number_patient, number_patient + number_hospital):
    name = fake.name()

    email = name.replace(" ", "").lower() + str(random.randint(11, 11111)) + "@gmail.com"
    p = email + "123456789"
    hash_object = hashlib.sha256(p.encode())
    pHash = hash_object.hexdigest()
    session.execute(User.insert().values({
        'userId': i,
        'email': email,
        'password_hash': pHash,
        'role': 'HOSPITAL'
    }))
    session.execute(Hospital.insert().values({
        'userId': i,
        'name': fake.city() + " Hospital",
        'address': fake.address(),
        'workingTime': 'Monday to Saturday from 8:00 AM to 5:00 PM',
        'point': round(random.uniform(1.5, 4.9), 1)
    }))

degree = ['Associate Professors Doctor', 'Master', 'PhD', 'Bachelor']
for i in range(number_patient + number_hospital, number_patient + number_hospital + number_doctor):
    name = fake.name()

    email = name.replace(" ", "").lower() + str(random.randint(11, 11111)) + "@gmail.com"
    p = email + "123456789"
    hash_object = hashlib.sha256(p.encode())
    pHash = hash_object.hexdigest()
    session.execute(User.insert().values({
        'userId': i,
        'email': email,
        'password_hash': pHash,
        'role': 'DOCTOR'
    }))
    consultingPriceViaMessage = random.randint(14, 19) + 0.99
    session.execute(Doctor.insert().values({
        'userId': i,
        'name': fake.name(),
        'age': random.randint(30, 53),
        'sex': sex[random.randint(0, len(sex) - 1)],
        'phone': '0' + fake.msisdn()[:9],
        'medicalSpecialtyId': random.randint(1, 20),
        'hospitalId': random.randint(1, number_hospital),
        'degree': degree[random.randint(0, len(degree) - 1)],
        'consultingPriceViaMessage': consultingPriceViaMessage,
        'consultingPriceViaCall': consultingPriceViaMessage + 13,
        'point': round(random.uniform(1.5, 4.9), 1)
    }))

session.commit()
session.close()