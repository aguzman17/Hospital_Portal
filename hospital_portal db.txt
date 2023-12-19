-- Create the hospital_portal database
CREATE DATABASE hospital_portal;

-- Use the hospital_portal database
USE hospital_portal;

-- Create the patients table
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(45) NOT NULL,
    age INT NOT NULL,
    admission_date DATE,
    discharge_date DATE
);

-- Create the doctors table
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(45) NOT NULL,
    specialization VARCHAR(45)
);

-- Insert sample data into the doctors table
INSERT INTO doctors (doctor_name, specialization)
VALUES
    ('Dr. Lopez', 'Cardiologist'),
    ('Dr. Johnson', 'Pediatrician'),
    ('Dr. Davis', 'Orthopedic'),
    ('Dr. Guzman', 'General'),
    ('Dr. Rodriguez', 'Neurologist');

-- Create the appointments table
CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Insert sample data into the patients table
INSERT INTO patients (patient_name, age, admission_date, discharge_date)
VALUES
    ('Maria Jozef', 67, '2023-10-01', '2023-10-07'),
    ('Abby Guzman', 23, '2023-11-15', '2023-11-20'),
    ('Jane Doe', 32, '2023-12-01', '2023-12-10');
    
-- Stored procedure for scheduling an appointment
DELIMITER //
CREATE PROCEDURE ScheduleAppointment(IN p_patient_id INT, IN p_doctor_id INT, IN p_appointment_date DATE, IN p_appointment_time DECIMAL(5, 2))
BEGIN
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time)
    VALUES (p_patient_id, p_doctor_id, p_appointment_date, p_appointment_time);
END //
DELIMITER ;

-- Stored procedure for discharging a patient
DELIMITER //
CREATE PROCEDURE DischargePatient(IN p_patient_id INT)
BEGIN
    UPDATE patients SET discharge_date = CURDATE() WHERE patient_id = p_patient_id;
END //
DELIMITER ;

-- Create a view joining doctors, appointments, and patients
CREATE VIEW doctors_appointments_patients_view AS
SELECT
    a.appointment_id,
    a.appointment_date,
    a.appointment_time,
    p.patient_id,
    p.patient_name,
    p.age,
    p.admission_date,
    p.discharge_date,
    d.doctor_id,
    d.doctor_name,
    d.specialization
FROM
    appointments a
JOIN
    patients p ON a.patient_id = p.patient_id
JOIN
    doctors d ON a.doctor_id = d.doctor_id;