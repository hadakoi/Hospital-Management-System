# Hospital Management System

A comprehensive Django-based Hospital Management System for managing patients, doctors, staff, appointments, and medical records.

## Features

### User Roles
- **Admin**: Full system access, manage all users and data
- **Doctor**: View appointments, create medical records, manage schedules
- **Patient**: Book appointments, view medical history
- **Staff/Receptionist**: Book appointments for patients, manage patient records

### Core Functionality
- Patient registration and management
- Doctor management with specialization and schedules
- Staff management
- Department management
- Appointment booking system with time slots
- Medical records with vitals and prescriptions
- Role-based dashboards
- Doctor availability management

## Project Structure

```
hospital_management/
├── hospital_management/     # Django project settings
├── hospital/               # Main application
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── forms.py           # Form definitions
│   ├── urls.py            # URL routing
│   ├── admin.py           # Django admin configuration
│   └── templates/         # HTML templates
├── templates/             # Global templates
├── static/               # Static files (CSS, JS)
├── manage.py            # Django management script
└── venv/               # Virtual environment
```

## Setup Instructions

### 1. Create Virtual Environment (if not already created)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install django crispy-bootstrap5
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

### 6. Access the Application

- Main Site: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## Default Passwords

When creating users through the admin or staff interface:
- **Patients**: `patient123`
- **Doctors**: `doctor123`
- **Staff**: `staff123`

## Quick Start Guide

### Setting up for Demo

1. **Create Admin Account**
   ```bash
   python manage.py createsuperuser
   ```
   Enter username, email, and password

2. **Login as Admin**
   - Go to http://127.0.0.1:8000/accounts/login/
   - Login with admin credentials
   - You'll be redirected to Admin Dashboard

3. **Create Departments** (Admin only)
   - From Admin Dashboard, click "Add Department"
   - Create departments like: Cardiology, Neurology, Pediatrics, General Medicine

4. **Add Doctors** (Admin only)
   - From Admin Dashboard, click "Add Doctor"
   - Fill in doctor details and assign to a department
   - Default password will be `doctor123`

5. **Add Doctor Schedules** (Admin or Doctor)
   - Go to Doctors list
   - Click on a doctor
   - Click "Add Schedule" to set available time slots

6. **Create Staff** (Admin only)
   - From Admin Dashboard, click "Add Staff"
   - Default password will be `staff123`

7. **Register Patients** (Self-registration or Staff)
   - Patients can self-register at http://127.0.0.1:8000/accounts/register/
   - Or staff can add patients from the dashboard

8. **Book Appointments** (Patient or Staff)
   - Patients: Go to Patient Dashboard → Book Appointment
   - Staff: Go to Patient list → Book Appointment for patient
   - Select doctor, date, and time (must match doctor's schedule)

9. **Confirm/Cancel Appointments** (Staff or Doctor)
   - Staff can confirm pending appointments
   - Staff/Doctors can update appointment status

10. **Create Medical Records** (Doctor only)
    - After completing an appointment, click "Create Medical Record"
    - Add diagnosis, prescription, vitals

## User Flows

### Patient Flow
1. Register/Login
2. View dashboard with upcoming appointments
3. Book new appointment (select doctor, date, time)
4. View medical records
5. Update profile

### Doctor Flow
1. Login
2. View dashboard with today's appointments
3. Update appointment status (confirm, complete, cancel)
4. Create medical records after appointments
5. View patient history

### Staff Flow
1. Login
2. View dashboard with all appointments
3. Add new patients
4. Book appointments for patients
5. Confirm/cancel appointments
6. View patient records

### Admin Flow
1. Login as superuser
2. Access full admin dashboard
3. Manage all users (patients, doctors, staff)
4. Manage departments
5. View system statistics

## Models Overview

| Model | Description |
|-------|-------------|
| UserProfile | Extended user with role management |
| Department | Hospital departments |
| Doctor | Doctor profiles with specialization |
| DoctorSchedule | Doctor availability by day/time |
| Patient | Patient profiles with medical info |
| Staff | Staff/receptionist profiles |
| Appointment | Booking system linking patient-doctor |
| MedicalRecord | Patient medical history |


## URLs Summary

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/accounts/register/` | Patient registration |
| `/dashboard/` | Role-based dashboard redirect |
| `/admin/dashboard/` | Admin dashboard |
| `/doctor/dashboard/` | Doctor dashboard |
| `/patient/dashboard/` | Patient dashboard |
| `/staff/dashboard/` | Staff dashboard |
| `/patients/` | Patient list |
| `/doctors/` | Doctor list |
| `/appointments/` | Appointment list |
| `/medical-records/` | Medical records list |
| `/admin/` | Django admin panel |

## Testing the System

### Test Accounts

You can create test accounts with different roles:

**Via Admin Panel (recommended)**
1. Login as admin
2. Go to Django admin: http://127.0.0.1:8000/admin/
3. Create users and assign roles through their profiles
4. Create associated Doctor/Patient/Staff records

**Via Command Line**
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from hospital.models import UserProfile, Department, Doctor

# Create a doctor
dept = Department.objects.create(name="Cardiology", description="Heart care")
user = User.objects.create_user('drsmith', 'smith@hospital.com', 'doctor123', first_name='John', last_name='Smith')
user.profile.role = 'doctor'
user.profile.save()
doctor = Doctor.objects.create(user=user, department=dept, specialization='Cardiologist', qualification='MD, PhD', experience_years=10, consultation_fee=150)
```

## Common Issues & Solutions

1. **"NoReverseMatch" errors**: Make sure you've run migrations
2. **Static files not loading**: Run `python manage.py collectstatic` (if DEBUG=False)
3. **Permission denied**: Check user role in UserProfile
4. **Can't book appointment**: Make sure doctor has schedule set up

## Technologies Used

- **Backend**: Django 5.x
- **Frontend**: Bootstrap 5
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Icons**: Bootstrap Icons
