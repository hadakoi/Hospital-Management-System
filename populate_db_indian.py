#!/usr/bin/env python
"""
Database Population Script for Hospital Management System - Indian Names
Run with: python populate_db_indian.py
"""

import os
import sys
import django

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
    print("Clearing existing data...")
    MedicalRecord.objects.all().delete()
    Appointment.objects.all().delete()
    Patient.objects.all().delete()
    DoctorSchedule.objects.all().delete()
    Doctor.objects.all().delete()
    Staff.objects.all().delete()
    Department.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("Data cleared.")


def create_departments():
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
    # Indian doctors data
    doctors_data = [
        {
            "username": "dr_sharma",
            "email": "sharma@hospital.com",
            "first_name": "Rajesh",
            "last_name": "Sharma",
            "dept_idx": 0,
            "specialization": "Cardiologist",
            "qualification": "MBBS, MD, DM (Cardiology)",
            "experience": 18,
            "fee": 800.00,
        },
        {
            "username": "dr_gupta",
            "email": "gupta@hospital.com",
            "first_name": "Priya",
            "last_name": "Gupta",
            "dept_idx": 0,
            "specialization": "Interventional Cardiologist",
            "qualification": "MBBS, MD, DM (Cardiology), FACC",
            "experience": 15,
            "fee": 1000.00,
        },
        {
            "username": "dr_patel",
            "email": "patel@hospital.com",
            "first_name": "Amit",
            "last_name": "Patel",
            "dept_idx": 1,
            "specialization": "Neurologist",
            "qualification": "MBBS, MD (Medicine), DM (Neurology)",
            "experience": 14,
            "fee": 700.00,
        },
        {
            "username": "dr_reddy",
            "email": "reddy@hospital.com",
            "first_name": "Lakshmi",
            "last_name": "Reddy",
            "dept_idx": 2,
            "specialization": "Pediatrician",
            "qualification": "MBBS, MD (Pediatrics)",
            "experience": 12,
            "fee": 600.00,
        },
        {
            "username": "dr_kumar",
            "email": "kumar@hospital.com",
            "first_name": "Vikram",
            "last_name": "Kumar",
            "dept_idx": 3,
            "specialization": "Orthopedic Surgeon",
            "qualification": "MBBS, MS (Orthopedics)",
            "experience": 16,
            "fee": 900.00,
        },
        {
            "username": "dr_iyer",
            "email": "iyer@hospital.com",
            "first_name": "Ananya",
            "last_name": "Iyer",
            "dept_idx": 4,
            "specialization": "General Physician",
            "qualification": "MBBS, MD (General Medicine)",
            "experience": 10,
            "fee": 500.00,
        },
        {
            "username": "dr_nair",
            "email": "nair@hospital.com",
            "first_name": "Suresh",
            "last_name": "Nair",
            "dept_idx": 5,
            "specialization": "Dermatologist",
            "qualification": "MBBS, MD (Dermatology)",
            "experience": 13,
            "fee": 650.00,
        },
        {
            "username": "dr_joshi",
            "email": "joshi@hospital.com",
            "first_name": "Meera",
            "last_name": "Joshi",
            "dept_idx": 6,
            "specialization": "Ophthalmologist",
            "qualification": "MBBS, MS (Ophthalmology)",
            "experience": 17,
            "fee": 750.00,
        },
        {
            "username": "dr_singh",
            "email": "singh@hospital.com",
            "first_name": "Arjun",
            "last_name": "Singh",
            "dept_idx": 7,
            "specialization": "ENT Specialist",
            "qualification": "MBBS, MS (ENT)",
            "experience": 11,
            "fee": 550.00,
        },
        {
            "username": "dr_desai",
            "email": "desai@hospital.com",
            "first_name": "Kavita",
            "last_name": "Desai",
            "dept_idx": 4,
            "specialization": "Diabetologist",
            "qualification": "MBBS, MD (Internal Medicine)",
            "experience": 14,
            "fee": 600.00,
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
        user.profile.phone = f"+91 98765{10000 + len(doctors):05d}"
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

        # Add schedule (Mon-Sat, 10AM-6PM)
        days = [0, 1, 2, 3, 4, 5]  # Monday to Saturday
        for day in days:
            DoctorSchedule.objects.create(
                doctor=doctor,
                day_of_week=day,
                start_time=time(10, 0),
                end_time=time(18, 0),
                is_available=True,
            )

    print(f"Created {len(doctors)} doctors with schedules.")
    return doctors


def create_staff(departments):
    staff_data = [
        {
            "username": "receptionist_rani",
            "email": "rani@hospital.com",
            "first_name": "Rani",
            "last_name": "Verma",
            "designation": "receptionist",
            "dept_idx": None,
        },
        {
            "username": "nurse_sunita",
            "email": "sunita@hospital.com",
            "first_name": "Sunita",
            "last_name": "Shah",
            "designation": "nurse",
            "dept_idx": 4,
        },
        {
            "username": "pharmacist_raj",
            "email": "raj@hospital.com",
            "first_name": "Raj",
            "last_name": "Malhotra",
            "designation": "pharmacist",
            "dept_idx": None,
        },
        {
            "username": "accountant_preeti",
            "email": "preeti@hospital.com",
            "first_name": "Preeti",
            "last_name": "Agarwal",
            "designation": "accountant",
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
        user.profile.phone = f"+91 87654{20000 + len(staff_members):05d}"
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
    # Indian patients data
    patients_data = [
        {
            "username": "patient_rahul",
            "email": "rahul.sharma@gmail.com",
            "first_name": "Rahul",
            "last_name": "Sharma",
            "dob": date(1985, 6, 15),
            "gender": "male",
            "blood": "O+",
            "phone": "+91 98765 43210",
            "address": "12 MG Road, Mumbai, Maharashtra",
        },
        {
            "username": "patient_neha",
            "email": "neha.gupta@gmail.com",
            "first_name": "Neha",
            "last_name": "Gupta",
            "dob": date(1990, 3, 22),
            "gender": "female",
            "blood": "A+",
            "phone": "+91 98765 43211",
            "address": "45 Rajpath, Delhi",
        },
        {
            "username": "patient_arjun",
            "email": "arjun.patel@gmail.com",
            "first_name": "Arjun",
            "last_name": "Patel",
            "dob": date(1975, 11, 8),
            "gender": "male",
            "blood": "B+",
            "phone": "+91 98765 43212",
            "address": "78 SG Highway, Ahmedabad, Gujarat",
        },
        {
            "username": "patient_priya",
            "email": "priya.reddy@gmail.com",
            "first_name": "Priya",
            "last_name": "Reddy",
            "dob": date(1995, 7, 30),
            "gender": "female",
            "blood": "AB+",
            "phone": "+91 98765 43213",
            "address": "23 Jubilee Hills, Hyderabad, Telangana",
        },
        {
            "username": "patient_vikram",
            "email": "vikram.kumar@gmail.com",
            "first_name": "Vikram",
            "last_name": "Kumar",
            "dob": date(1980, 12, 5),
            "gender": "male",
            "blood": "O-",
            "phone": "+91 98765 43214",
            "address": "56 Anna Salai, Chennai, Tamil Nadu",
        },
        {
            "username": "patient_ananya",
            "email": "ananya.iyer@gmail.com",
            "first_name": "Ananya",
            "last_name": "Iyer",
            "dob": date(1988, 9, 18),
            "gender": "female",
            "blood": "A-",
            "phone": "+91 98765 43215",
            "address": "89 Residency Road, Bangalore, Karnataka",
        },
        {
            "username": "patient_suresh",
            "email": "suresh.nair@gmail.com",
            "first_name": "Suresh",
            "last_name": "Nair",
            "dob": date(1970, 4, 12),
            "gender": "male",
            "blood": "B-",
            "phone": "+91 98765 43216",
            "address": "34 Marine Drive, Kochi, Kerala",
        },
        {
            "username": "patient_meera",
            "email": "meera.joshi@gmail.com",
            "first_name": "Meera",
            "last_name": "Joshi",
            "dob": date(1992, 1, 25),
            "gender": "female",
            "blood": "O+",
            "phone": "+91 98765 43217",
            "address": "67 FC Road, Pune, Maharashtra",
        },
        {
            "username": "patient_aditya",
            "email": "aditya.desai@gmail.com",
            "first_name": "Aditya",
            "last_name": "Desai",
            "dob": date(1983, 8, 14),
            "gender": "male",
            "blood": "A+",
            "phone": "+91 98765 43218",
            "address": "90 Law Garden, Ahmedabad, Gujarat",
        },
        {
            "username": "patient_kavita",
            "email": "kavita.singh@gmail.com",
            "first_name": "Kavita",
            "last_name": "Singh",
            "dob": date(1987, 5, 20),
            "gender": "female",
            "blood": "B+",
            "phone": "+91 98765 43219",
            "address": "11 Gomti Nagar, Lucknow, Uttar Pradesh",
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
        user.profile.address = pat_data["address"]
        user.profile.save()

        patient = Patient.objects.create(
            user=user,
            date_of_birth=pat_data["dob"],
            gender=pat_data["gender"],
            blood_group=pat_data["blood"],
            emergency_contact_name=f"Emergency Contact - {pat_data['last_name']}",
            emergency_contact_phone=f"+91 98765 {30000 + len(patients):05d}",
            medical_history="",
        )
        patients.append(patient)

    print(f"Created {len(patients)} patients.")
    return patients


def create_appointments(patients, doctors):
    appointments_data = [
        # (patient_idx, doctor_idx, days_offset, hour, status, symptoms)
        (0, 0, 1, 11, "confirmed", "Chest pain and breathlessness during walking"),
        (1, 2, 1, 14, "pending", "Severe headaches and dizziness since last week"),
        (2, 3, 2, 10, "confirmed", "High fever with cough and cold symptoms"),
        (3, 5, 2, 16, "pending", "Annual health checkup and diabetes review"),
        (4, 4, 3, 11, "confirmed", "Knee pain after playing cricket"),
        (5, 6, 3, 14, "pending", "Skin rash and itching on arms"),
        (6, 7, 4, 12, "confirmed", "Blurry vision in left eye"),
        (7, 0, 4, 17, "pending", "Heart palpitations and anxiety"),
        (8, 5, 5, 10, "confirmed", "High blood sugar levels"),
        (9, 8, 5, 15, "pending", "Sinusitis and ear pain"),
        # Past appointments (completed)
        (0, 5, -5, 11, "completed", "Fever and body ache"),
        (1, 6, -7, 14, "completed", "Acne treatment follow-up"),
        (2, 4, -10, 12, "completed", "Back pain consultation"),
        (3, 2, -3, 10, "completed", "Child vaccination"),
        # Cancelled appointments
        (4, 7, -2, 15, "cancelled", "Migraine episodes"),
        (5, 3, -1, 11, "cancelled", "Fever and weakness"),
    ]

    appointments = []
    for app_data in appointments_data:
        patient = patients[app_data[0]]
        doctor = doctors[app_data[1]]
        app_date = date.today() + timedelta(days=app_data[2])
        app_time = time(app_data[3], 0)

        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            scheduled_by=patient.user,
            appointment_date=app_date,
            appointment_time=app_time,
            status=app_data[4],
            symptoms=app_data[5],
            notes=""
            if app_data[4] != "cancelled"
            else "Patient requested to reschedule",
        )
        appointments.append(appointment)

    print(f"Created {len(appointments)} appointments.")
    return appointments


def create_medical_records(appointments, doctors):
    records_data = [
        {
            "appointment_idx": 10,
            "diagnosis": "Viral fever with upper respiratory tract infection",
            "prescription": "Tab. Crocin 650mg - 1 tab 3 times daily for 5 days\nTab. Azithral 500mg - 1 tab daily for 3 days\nPlenty of fluids and rest",
            "bp": "130/85",
            "temp": 38.2,
            "weight": 72.5,
            "heart_rate": 88,
            "notes": "Patient advised to avoid cold food and drinks",
        },
        {
            "appointment_idx": 11,
            "diagnosis": "Moderate acne vulgaris with post-inflammatory hyperpigmentation",
            "prescription": "Benzac AC 2.5% gel - apply at night\nAhaglow face wash - twice daily\nSunscreen SPF 50 - morning",
            "bp": "115/75",
            "temp": 36.7,
            "weight": 58.0,
            "heart_rate": 72,
            "notes": "Follow up after 1 month",
        },
        {
            "appointment_idx": 12,
            "diagnosis": "Lumbar muscle strain - Grade 1",
            "prescription": "Tab. Myospaz Forte - 1 tab twice daily for 7 days\nVolini spray - 3 times daily\nPhysiotherapy recommended",
            "bp": "125/80",
            "temp": 36.8,
            "weight": 78.3,
            "heart_rate": 76,
            "notes": "Avoid lifting heavy weights for 3 weeks",
        },
        {
            "appointment_idx": 13,
            "diagnosis": "Routine immunization - DPT booster dose administered",
            "prescription": "Paracetamol syrup - if fever develops\nNext vaccination due after 1 year",
            "bp": "100/65",
            "temp": 36.5,
            "weight": 18.5,
            "heart_rate": 95,
            "notes": "Child healthy and active",
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
            follow_up_date=date.today() + timedelta(days=30),
        )
        records.append(record)

    print(f"Created {len(records)} medical records.")
    return records


def print_summary():
    print("\n" + "=" * 60)
    print("  HOSPITAL MANAGEMENT SYSTEM - DATABASE POPULATED")
    print("=" * 60)
    print(f"  Departments:       {Department.objects.count()}")
    print(f"  Doctors:           {Doctor.objects.count()}")
    print(f"  Staff:             {Staff.objects.count()}")
    print(f"  Patients:          {Patient.objects.count()}")
    print(f"  Appointments:      {Appointment.objects.count()}")
    print(f"  Medical Records:   {MedicalRecord.objects.count()}")
    print("=" * 60)

    print("\n  TEST ACCOUNTS:")
    print("-" * 60)
    print("  Admin:      admin / admin123")
    print("  Doctors:    dr_sharma, dr_gupta, dr_patel, etc. / doctor123")
    print("  Staff:      receptionist_rani, nurse_sunita, etc. / staff123")
    print("  Patients:   patient_rahul, patient_neha, etc. / patient123")
    print("=" * 60)


def main():
    print("Starting database population with Indian names...\n")

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
