DROP SCHEMA IF EXISTS momcare;
CREATE SCHEMA momcare;
USE momcare;

CREATE TABLE User (
    userId BIGINT NOT NULL AUTO_INCREMENT,
    email VARCHAR(128) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role ENUM('ADMIN', 'PATIENT', 'DOCTOR', 'HOSPITAL') NOT NULL,
    googleId VARCHAR(128) DEFAULT NULL,
    UNIQUE(email),
    PRIMARY KEY (userId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Patient (
    patientId BIGINT NOT NULL AUTO_INCREMENT,
    userId BIGINT,
    name VARCHAR(100) NOT NULL,
    age INT DEFAULT NULL,
    sex ENUM('MALE', 'FEMALE', 'NOT_MENTION') DEFAULT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    address TEXT DEFAULT NULL,
    PRIMARY KEY (patientId),
    CONSTRAINT fk_User_Patient FOREIGN KEY (userId) REFERENCES User (userId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Hospital (
    hospitalId BIGINT NOT NULL AUTO_INCREMENT,
    userId BIGINT,
    name VARCHAR(500) NOT NULL,
    address TEXT DEFAULT NULL,
    workingTime TEXT DEFAULT NULL,
    point FLOAT DEFAULT NULL,
    PRIMARY KEY (hospitalId),
    CONSTRAINT fk_User_Hospital FOREIGN KEY (userId) REFERENCES User (userId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE MedicalSpecialty (
    medicalSpecialtyId INT NOT NULL AUTO_INCREMENT,
    englishName VARCHAR(100) DEFAULT NULL,
    vietnameseName VARCHAR(100) DEFAULT NULL,
    PRIMARY KEY (medicalSpecialtyId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Doctor (
    doctorId BIGINT NOT NULL AUTO_INCREMENT,
    userId BIGINT,
    `name` VARCHAR(100) NOT NULL,
    age INT DEFAULT NULL,
    sex ENUM('MALE', 'FEMALE', 'NOT_MENTION') DEFAULT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    medicalSpecialtyId INT DEFAULT NULL,
    hospitalId BIGINT DEFAULT NULL,
    degree VARCHAR(300) DEFAULT NULL,
    consultingPriceViaMessage FLOAT DEFAULT 0,
    consultingPriceViaCall FLOAT DEFAULT 0,
    `point` FLOAT DEFAULT NULL,
    PRIMARY KEY (doctorId),
    CONSTRAINT fk_Doctor_MedicalSpecialty FOREIGN KEY (medicalSpecialtyId) REFERENCES MedicalSpecialty (medicalSpecialtyId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Doctor_Hospital FOREIGN KEY (hospitalId) REFERENCES Hospital (hospitalId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Doctor_User FOREIGN KEY (userId) REFERENCES User (userId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE DoctorComment (
    doctorCommentId BIGINT NOT NULL AUTO_INCREMENT,
    time DATETIME DEFAULT NULL,
    patientId BIGINT NOT NULL,
    doctorId BIGINT NOT NULL,
    comment TEXT DEFAULT NULL,
    point FLOAT DEFAULT NULL,
    PRIMARY KEY (doctorCommentId),
    CONSTRAINT fk_DoctorComment_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_DoctorComment_Doctor FOREIGN KEY (doctorId) REFERENCES Doctor (doctorId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE HospitalComment (
    hospitalCommentId BIGINT NOT NULL AUTO_INCREMENT,
    time DATETIME DEFAULT NULL,
    patientId BIGINT NOT NULL,
    hospitalId BIGINT NOT NULL,
    comment TEXT DEFAULT NULL,
    point FLOAT DEFAULT NULL,
    PRIMARY KEY (hospitalCommentId),
    CONSTRAINT fk_HospitalComment_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_HospitalComment_Hospital FOREIGN KEY (hospitalId) REFERENCES Hospital (hospitalId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Conversation (
    conversationId BIGINT NOT NULL AUTO_INCREMENT,
    patientId BIGINT NOT NULL,
    doctorId BIGINT NOT NULL,
    startTime DATETIME DEFAULT NULL,
    state ENUM('CLOSED', 'KEEP') DEFAULT NULL,
    PRIMARY KEY (conversationId),
    CONSTRAINT fk_Conversation_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Conversation_Doctor FOREIGN KEY (doctorId) REFERENCES Doctor (doctorId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Message (
    messageId BIGINT NOT NULL AUTO_INCREMENT,
    conversationId BIGINT NOT NULL,
    sender BIGINT NOT NULL,
    text TEXT DEFAULT NULL,
    time DATETIME DEFAULT NULL,
    state ENUM('SEEN', 'NOT_SEEN') DEFAULT NULL,
    PRIMARY KEY (messageId),
    CONSTRAINT fk_Message_Conversation FOREIGN KEY (conversationId) REFERENCES Conversation (conversationId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Message_User FOREIGN KEY (sender) REFERENCES User (userId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Attachment (
    attachmentId BIGINT NOT NULL AUTO_INCREMENT,
    conversationId BIGINT NOT NULL,
    sender BIGINT NOT NULL,
    `file` VARCHAR(500) DEFAULT NULL,
    `time` DATETIME DEFAULT NULL,
    state ENUM('SEEN', 'NOT_SEEN') DEFAULT NULL,
    PRIMARY KEY (attachmentId),
    CONSTRAINT fk_Attachment_Conversation FOREIGN KEY (conversationId) REFERENCES Conversation (conversationId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Attachment_User FOREIGN KEY (sender) REFERENCES User (userId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE CallAppointment (
    callAppointmentId BIGINT NOT NULL AUTO_INCREMENT,
    time DATETIME DEFAULT NULL,
    form VARCHAR(128) DEFAULT NULL,
    doctorId BigINT NOT NULL,
    patientId BIGINT NOT NULL,
    state ENUM('CONFIRM', 'UNCOMFIRM', 'COMPLETED') DEFAULT NULL,
    PRIMARY KEY (callAppointmentId),
    CONSTRAINT fk_CallAppointment_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_CallAppointment_Doctor FOREIGN KEY (doctorId) REFERENCES Doctor (doctorId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Call` (
    callId BIGINT NOT NULL AUTO_INCREMENT,
    callAppointmentId BIGINT NOT NULL,
    problems TEXT DEFAULT NULL,
    startTime DATETIME DEFAULT NULL,
    endTime DATETIME DEFAULT NULL,
    link VARCHAR(500) DEFAULT NULL,
    PRIMARY KEY (callId),
    CONSTRAINT fk_Call_CallAppointment FOREIGN KEY (callAppointmentId) REFERENCES CallAppointment (callAppointmentId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE HospitalAppointment (
    hospitalAppointmentId BIGINT NOT NULL AUTO_INCREMENT,
    time DATETIME DEFAULT NULL,
    hospitalId BIGINT NOT NULL,
    patientId BIGINT NOT NULL,
    state ENUM('CONFIRM', 'UNCOMFIRM', 'COMPLETED') DEFAULT NULL,
    PRIMARY KEY (hospitalAppointmentId),
    CONSTRAINT fk_HospitalAppointment_Hospital FOREIGN KEY (hospitalId) REFERENCES Hospital (hospitalId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_HospitalAppointment_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE MedicalHistory (
    medicalHistoryId BIGINT NOT NULL AUTO_INCREMENT,
    patientId BIGINT NOT NULL,
    symptom TEXT DEFAULT NULL,
    existingDiseases TEXT DEFAULT NULL,
    PRIMARY KEY (medicalHistoryId),
    CONSTRAINT fk_MedicalHistory_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE MedicalRecord (
    medicalRecordId BIGINT NOT NULL AUTO_INCREMENT,
    patientId BIGINT NOT NULL,
    doctorId BIGINT NOT NULL,
    `time` DATETIME DEFAULT NULL,
    medicalHistoryId BIGINT NOT NULL,
    diagnostic TEXT DEFAULT NULL,
    note TEXT DEFAULT NULL,
    PRIMARY KEY (medicalRecordId),
    CONSTRAINT fk_MedicalRecord_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_MedicalRecord_Doctor FOREIGN KEY (doctorId) REFERENCES Doctor (doctorId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_MedicalRecord_MedicalHistory FOREIGN KEY (medicalHistoryId) REFERENCES MedicalHistory (medicalHistoryId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Prescription (
    prescriptionId BIGINT NOT NULL AUTO_INCREMENT,
    medicalRecordId BIGINT NOT NULL,
    medicinesNameAndDosages TEXT DEFAULT NULL,
    usageTime TEXT DEFAULT NULL,
    note TEXT DEFAULT NULL,
    PRIMARY KEY (prescriptionId),
    CONSTRAINT fk_Prescription_MedicalRecord FOREIGN KEY (medicalRecordId) REFERENCES MedicalRecord (medicalRecordId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE Invoice (
    invoiceId BIGINT NOT NULL AUTO_INCREMENT,
    consultingServices ENUM('MESSAGE', 'CALL', 'BOTH') DEFAULT NULL,
    callAppointmentId BIGINT DEFAULT NULL,
    conversationId BIGINT DEFAULT NULL,
    `time` DATETIME DEFAULT NULL,
    dueTime DATETIME DEFAULT NULL,
    totalAmount FLOAT DEFAULT NULL,
    note TEXT DEFAULT NULL,
    status ENUM('PAID', 'UNPAID', 'PAST_DUE') DEFAULT NULL,
    PRIMARY KEY (invoiceId),
    CONSTRAINT fk_Invoice_CallAppointment FOREIGN KEY (callAppointmentId) REFERENCES CallAppointment (callAppointmentId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Invoice_Conversation FOREIGN KEY (conversationId) REFERENCES Conversation (conversationId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Payment (
    paymentId BIGINT NOT NULL AUTO_INCREMENT,
    patientId BIGINT NOT NULL,
    amount FLOAT DEFAULT NULL,
    paymentTime DATETIME DEFAULT NULL,
    status ENUM('PAID', 'FAILED') DEFAULT NULL,
    paymentMethod ENUM('CASH', 'BANKING') DEFAULT NULL,
    PRIMARY KEY (paymentId),
    CONSTRAINT fk_Payment_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Transaction` (
    transactionId BIGINT NOT NULL AUTO_INCREMENT,
    invoiceId BIGINT NOT NULL,
    paymentId BIGINT NOT NULL,
    `time` DATETIME DEFAULT NULL,
    amount FLOAT DEFAULT NULL,
    `description` TEXT DEFAULT NULL,
    PRIMARY KEY (transactionId),
    CONSTRAINT fk_Transaction_Invoice FOREIGN KEY (invoiceId) REFERENCES Invoice (invoiceId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Transaction_Payment FOREIGN KEY (paymentId) REFERENCES Payment (paymentId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Token (
    userId BIGINT NOT NULL,
    token VARCHAR(300) NOT NULL,
    expires BOOLEAN,
    PRIMARY KEY (token),
    CONSTRAINT fk_Token_User FOREIGN KEY (userId) REFERENCES User (userId) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `MedicalSpecialty` VALUES
(1,'Internal Medicine','Nội Khoa'),
(2,'Pediatrics','Nhi Khoa'),
(3,'Surgery','Phẫu Thuật'),
(4,'Obstetrics and Gynecology','Sản Khoa và Phụ Nữ Học'),
(5,'Orthopedics','Chấn Thương Chỉnh Hình'),
(6,'Dermatology','Da Liễu Học'),
(7,'Ophthalmology','Mắt Học'),
(8,'Otolaryngology','Tai Mũi Họng'),
(9,'Neurology','Thần Kinh Học'),
(10,'Psychiatry','Tâm Thần Học'),
(11,'Anesthesiology','Sư Phạm Y Học'),
(12,'Radiology','Xét Nghiệm Hình Ảnh Y Học'),
(13,'Emergency Medicine','Y Học Cấp Cứu'),
(14,'Cardiology','Tim Mạch Học'),
(15,'Gastroenterology','Nội Tiêu Hóa Học'),
(16,'Urology','Tiểu Nhi Học'),
(17,'Nephrology','Thận Học'),
(18,'Hematology','Huyết Học'),
(19,'Oncology','Ung Thư Học'),
(20,'Rheumatology','Thấp Khớp Học');