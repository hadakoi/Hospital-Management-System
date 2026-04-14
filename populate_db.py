#!/usr/bin/env python
"""
Database Population Script for Hospital Management System
Run with: python populate_db.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hospital_management.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from datetime import date, time, timedelta
from django.contrib.auth.models import User
from hospital.models import (
    Department,
    Doctor,
    DoctorSchedule,
    Patient,
    Staff,
    Appointment,
    MedicalRecord,
)


def clear_existing_data():
    """Clear existing test data but keep admin"""
    print("Clearing existing data...")
    MedicalRecord.objects.all().delete()
    Appointment.objects.all().delete()
    Patient.objects.all().delete()
    DoctorSchedule.objects.all().delete()
    Doctor.objects.all().delete()
    Staff.objects.all().delete()

    # Delete non-admin users
    User.objects.filter(is_superuser=False).delete()
    print("Data cleared.")


def create_departments():
    """Create hospital departments"""
    departments_data = [
        (
            "Cardiology",
            "Heart and cardiovascular system care, including heart disease treatment and prevention.",
        ),
        (
            "Neurology",
            "Brain, spine, and nervous system disorders diagnosis and treatment.",
        ),
        (
            "Pediatrics",
            "Healthcare for infants, children, and adolescents up to age 18.",
        ),
        (
            "Orthopedics",
            "Musculoskeletal system care including bones, joints, muscles, and ligaments.",
        ),
        (
            "General Medicine",
            "Primary care, general health checkups, and common illness treatment.",
        ),
        ("Dermatology", "Skin, hair, and nail conditions diagnosis and treatment."),
        (
            "Ophthalmology",
            "Eye and vision care, including eye surgery and disease treatment.",
        ),
        ("ENT", "Ear, nose, and throat conditions treatment and surgery."),
    ]

    depts = []
    for name, desc in departments_data:
        dept, _ = Department.objects.get_or_create(
            name=name, defaults={"description": desc}
        )
        depts.append(dept)

    print(f"Created {len(depts)} departments.")
    return depts


def create_doctors(departments):
    """Create doctors with schedules"""
    doctors_data = [
        {
            "username": "dr_smith",
            "email": "smith@hospital.com",
            "first_name": "John",
            "last_name": "Smith",
            "dept_idx": 0,
            "specialization": "Cardiologist",
            "qualification": "MD, FACC",
            "experience": 15,
            "fee": 250.00,
        },
        {
            "username": "dr_johnson",
            "email": "johnson@hospital.com",
            "first_name": "Sarah",
            "last_name": "Johnson",
            "dept_idx": 0,
            "specialization": "Cardiac Surgeon",
            "qualification": "MD, PhD, FACS",
            "experience": 20,
            "fee": 350.00,
        },
        {
            "username": "dr_williams",
            "email": "williams@hospital.com",
            "first_name": "Michael",
            "last_name": "Williams",
            "dept_idx": 1,
            "specialization": "Neurologist",
            "qualification": "MD, FAAN",
            "experience": 12,
            "fee": 200.00,
        },
        {
            "username": "dr_brown",
            "email": "brown@hospital.com",
            "first_name": "Emily",
            "last_name": "Brown",
            "dept_idx": 2,
            "specialization": "Pediatrician",
            "qualification": "MD, FAAP",
            "experience": 10,
            "fee": 180.00,
        },
        {
            "username": "dr_davis",
            "email": "davis@hospital.com",
            "first_name": "Robert",
            "last_name": "Davis",
            "dept_idx": 3,
            "specialization": "Orthopedic Surgeon",
            "qualification": "MD, FAAOS",
            "experience": 18,
            "fee": 300.00,
        },
        {
            "username": "dr_miller",
            "email": "miller@hospital.com",
            "first_name": "Jennifer",
            "last_name": "Miller",
            "dept_idx": 4,
            "specialization": "General Physician",
            "qualification": "MD",
            "experience": 8,
            "fee": 150.00,
        },
        {
            "username": "dr_wilson",
            "email": "wilson@hospital.com",
            "first_name": "David",
            "last_name": "Wilson",
            "dept_idx": 5,
            "specialization": "Dermatologist",
            "qualification": "MD, FAAD",
            "experience": 14,
            "fee": 220.00,
        },
        {
            "username": "dr_moore",
            "email": "moore@hospital.com",
            "first_name": "Lisa",
            "last_name": "Moore",
            "dept_idx": 6,
            "specialization": "Ophthalmologist",
            "qualification": "MD, FACS",
            "experience": 16,
            "fee": 280.00,
        },
    ]

    doctors = []
    for doc_data in doctors_data:
        user = User.objects.create_user(
            username=doc_data["username"],
            email=doc_data["email"],
            first_name=doc_data["first_name"],
            last_name=doc_data["last_name"],
            password="doctor123",
        )
        user.profile.role = "doctor"
        user.profile.phone = f"555-{1000 + len(doctors)}"
        user.profile.save()

        doctor = Doctor.objects.create(
            user=user,
            department=departments[doc_data["dept_idx"]],
            specialization=doc_data["specialization"],
            qualification=doc_data["qualification"],
            experience_years=doc_data["experience"],
            consultation_fee=doc_data["fee"],
            is_active=True,
        )
        doctors.append(doctor)

        # Add schedule (Mon-Fri, 9AM-5PM with different slots)
        days = [0, 1, 2, 3, 4]  # Monday to Friday
        for day in days:
            DoctorSchedule.objects.create(
                doctor=doctor,
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(17, 0),
                is_available=True,
            )

    print(f"Created {len(doctors)} doctors with schedules.")
    return doctors


def create_staff(departments):
    """Create staff members"""
    staff_data = [
        {
            "username": "receptionist1",
            "email": "reception@hospital.com",
            "first_name": "Mary",
            "last_name": "Taylor",
            "designation": "receptionist",
            "dept_idx": None,
        },
        {
            "username": "nurse1",
            "email": "nurse@hospital.com",
            "first_name": "Patricia",
            "last_name": "Anderson",
            "designation": "nurse",
            "dept_idx": 4,
        },
        {
            "username": "pharmacist1",
            "email": "pharma@hospital.com",
            "first_name": "James",
            "last_name": "Thomas",
            "designation": "pharmacist",
            "dept_idx": None,
        },
    ]

    staff_members = []
    for staff_item in staff_data:
        user = User.objects.create_user(
            username=staff_item["username"],
            email=staff_item["email"],
            first_name=staff_item["first_name"],
            last_name=staff_item["last_name"],
            password="staff123",
        )
        user.profile.role = "staff"
        user.profile.phone = f"555-{2000 + len(staff_members)}"
        user.profile.save()

        dept = (
            departments[staff_item["dept_idx"]]
            if staff_item["dept_idx"] is not None
            else None
        )
        staff = Staff.objects.create(
            user=user,
            designation=staff_item["designation"],
            department=dept,
            is_active=True,
        )
        staff_members.append(staff)

    print(f"Created {len(staff_members)} staff members.")
    return staff_members


def create_patients():
    """Create patients"""
    patients_data = [
        {
            "username": "patient_john",
            "email": "john.doe@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "dob": date(1985, 6, 15),
            "gender": "male",
            "blood": "O+",
            "phone": "555-3001",
        },
        {
            "username": "patient_jane",
            "email": "jane.smith@gmail.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "dob": date(1990, 3, 22),
            "gender": "female",
            "blood": "A+",
            "phone": "555-3002",
        },
        {
            "username": "patient_bob",
            "email": "bob.wilson@gmail.com",
            "first_name": "Bob",
            "last_name": "Wilson",
            "dob": date(1975, 11, 8),
            "gender": "male",
            "blood": "B+",
            "phone": "555-3003",
        },
        {
            "username": "patient_alice",
            "email": "alice.brown@gmail.com",
            "first_name": "Alice",
            "last_name": "Brown",
            "dob": date(1995, 7, 30),
            "gender": "female",
            "blood": "AB+",
            "phone": "555-3004",
        },
        {
            "username": "patient_charlie",
            "email": "charlie.davis@gmail.com",
            "first_name": "Charlie",
            "last_name": "Davis",
            "dob": date(1980, 12, 5),
            "gender": "male",
            "blood": "O-",
            "phone": "555-3005",
        },
        {
            "username": "patient_eve",
            "email": "eve.miller@gmail.com",
            "first_name": "Eve",
            "last_name": "Miller",
            "dob": date(1988, 9, 18),
            "gender": "female",
            "blood": "A-",
            "phone": "555-3006",
        },
        {
            "username": "patient_frank",
            "email": "frank.taylor@gmail.com",
            "first_name": "Frank",
            "last_name": "Taylor",
            "dob": date(1970, 4, 12),
            "gender": "male",
            "blood": "B-",
            "phone": "555-3007",
        },
        {
            "username": "patient_grace",
            "email": "grace.anderson@gmail.com",
            "first_name": "Grace",
            "last_name": "Anderson",
            "dob": date(1992, 1, 25),
            "gender": "female",
            "blood": "O+",
            "phone": "555-3008",
        },
    ]

    patients = []
    for pat_data in patients_data:
        user = User.objects.create_user(
            username=pat_data["username"],
            email=pat_data["email"],
            first_name=pat_data["first_name"],
            last_name=pat_data["last_name"],
            password="patient123",
        )
        user.profile.role = "patient"
        user.profile.phone = pat_data["phone"]
        user.profile.save()

        patient = Patient.objects.create(
            user=user,
            date_of_birth=pat_data["dob"],
            gender=pat_data["gender"],
            blood_group=pat_data["blood"],
            emergency_contact_name=f"Emergency Contact {pat_data['last_name']}",
            emergency_contact_phone=f"555-{4000 + len(patients)}",
            medical_history="",
        )
        patients.append(patient)

    print(f"Created {len(patients)} patients.")
    return patients


def create_appointments(patients, doctors):
    """Create appointments"""
    appointments_data = [
        # (patient_idx, doctor_idx, days_offset, hour, status, symptoms)
        (0, 0, 1, 10, "confirmed", "Chest pain and shortness of breath"),
        (1, 2, 1, 14, "pending", "Severe headaches and dizziness"),
        (2, 3, 2, 11, "confirmed", "Fever and cough"),
        (3, 5, 2, 15, "pending", "Annual health checkup"),
        (4, 4, 3, 9, "confirmed", "Knee pain after sports injury"),
        (5, 6, 3, 13, "pending", "Skin rash on arms"),
        (6, 7, 4, 10, "confirmed", "Blurry vision in right eye"),
        (7, 0, 4, 16, "pending", "Heart palpitations"),
        (0, 5, -2, 10, "completed", "Fever and cold symptoms"),
        (1, 6, -3, 14, "completed", "Acne treatment follow-up"),
        (2, 4, -5, 11, "completed", "Back pain consultation"),
        (3, 2, -1, 9, "cancelled", "Migraine episodes"),
    ]

    appointments = []
    for app_data in appointments_data:
        patient = patients[app_data[0]]
        doctor = doctors[app_data[1]]
        app_date = date.today() + timedelta(days=app_data[2])
        app_time = time(app_data[3], 0)

        # Only create if date is in future or status is completed/cancelled
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            scheduled_by=patient.user,
            appointment_date=app_date,
            appointment_time=app_time,
            status=app_data[4],
            symptoms=app_data[5],
            notes="" if app_data[4] != "cancelled" else "Patient requested reschedule",
        )
        appointments.append(appointment)

    print(f"Created {len(appointments)} appointments.")
    return appointments


def create_medical_records(appointments, doctors):
    """Create medical records for completed appointments"""
    records_data = [
        {
            "appointment_idx": 8,
            "diagnosis": "Common cold with mild fever",
            "prescription": "Paracetamol 500mg - 1 tablet 3 times daily for 5 days\nVitamin C - 1 tablet daily\nPlenty of rest and fluids",
            "bp": "120/80",
            "temp": 37.2,
            "weight": 75.5,
            "heart_rate": 72,
            "notes": "Patient responding well to treatment",
        },
        {
            "appointment_idx": 9,
            "diagnosis": "Moderate acne vulgaris",
            "prescription": "Benzoyl Peroxide gel - apply at night\nSalicylic acid face wash - twice daily",
            "bp": "110/70",
            "temp": 36.8,
            "weight": 62.0,
            "heart_rate": 68,
            "notes": "Follow up in 4 weeks",
        },
        {
            "appointment_idx": 10,
            "diagnosis": "Lower back muscle strain",
            "prescription": "Ibuprofen 400mg - 1 tablet twice daily for 7 days\nMuscle relaxant - as needed\nPhysical therapy recommended",
            "bp": "125/82",
            "temp": 36.9,
            "weight": 82.3,
            "heart_rate": 74,
            "notes": "Avoid heavy lifting for 2 weeks",
        },
    ]

    records = []
    for rec_data in records_data:
        appointment = appointments[rec_data["appointment_idx"]]

        record = MedicalRecord.objects.create(
            patient=appointment.patient,
            doctor=appointment.doctor,
            appointment=appointment,
            diagnosis=rec_data["diagnosis"],
            symptoms=appointment.symptoms,
            prescription=rec_data["prescription"],
            notes=rec_data["notes"],
            blood_pressure=rec_data["bp"],
            temperature=rec_data["temp"],
            weight=rec_data["weight"],
            heart_rate=rec_data["heart_rate"],
            follow_up_date=date.today() + timedelta(days=14),
        )
        records.append(record)

    print(f"Created {len(records)} medical records.")
    return records


def print_summary():
    """Print database summary"""
    print("\n" + "=" * 50)
    print("DATABASE POPULATION COMPLETE")
    print("=" * 50)
    print(f"Departments:       {Department.objects.count()}")
    print(f"Doctors:           {Doctor.objects.count()}")
    print(f"Staff:             {Staff.objects.count()}")
    print(f"Patients:          {Patient.objects.count()}")
    print(f"Appointments:      {Appointment.objects.count()}")
    print(f"Medical Records:   {MedicalRecord.objects.count()}")
    print("=" * 50)

    print("\nTEST ACCOUNTS:")
    print("-" * 50)
    print("Admin:      admin / admin123")
    print("Doctors:    dr_smith, dr_johnson, dr_williams, etc. / doctor123")
    print("Staff:      receptionist1, nurse1, pharmacist1 / staff123")
    print("Patients:   patient_john, patient_jane, etc. / patient123")
    print("=" * 50)


def main():
    print("Starting database population...\n")

    clear_existing_data()
    departments = create_departments()
    doctors = create_doctors(departments)
    staff = create_staff(departments)
    patients = create_patients()
    appointments = create_appointments(patients, doctors)
    records = create_medical_records(appointments, doctors)

    print_summary()
    print("\nDone! You can now start the server and test the application.")


if __name__ == "__main__":
    main()
