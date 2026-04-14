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

## Quick Start

### 1. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Populate Database (Creates Test Data with Indian Names)

```bash
python populate_db_indian.py
```

This creates:
- 8 departments
- 10 doctors with Indian names and schedules
- 4 staff members with Indian names
- 10 patients with Indian names
- 16 appointments (pending, confirmed, completed, cancelled)
- 4 medical records

### 5. Create Admin (If Not Using populate_db_indian.py)

```bash
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

### 7. Access Application

- Main Site: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## Test Credentials (Indian Names)

### Admin
| Username | Password |
|----------|----------|
| admin | admin123 |

### Doctors
| Username | Password | Name | Specialization |
|----------|----------|------|----------------|
| dr_sharma | doctor123 | Dr. Rajesh Sharma | Cardiologist |
| dr_gupta | doctor123 | Dr. Priya Gupta | Interventional Cardiologist |
| dr_patel | doctor123 | Dr. Amit Patel | Neurologist |
| dr_reddy | doctor123 | Dr. Lakshmi Reddy | Pediatrician |
| dr_kumar | doctor123 | Dr. Vikram Kumar | Orthopedic Surgeon |
| dr_iyer | doctor123 | Dr. Ananya Iyer | General Physician |
| dr_nair | doctor123 | Dr. Suresh Nair | Dermatologist |
| dr_joshi | doctor123 | Dr. Meera Joshi | Ophthalmologist |
| dr_singh | doctor123 | Dr. Arjun Singh | ENT Specialist |
| dr_desai | doctor123 | Dr. Kavita Desai | Diabetologist |

### Staff
| Username | Password | Name | Role |
|----------|----------|------|------|
| receptionist_rani | staff123 | Rani Verma | Receptionist |
| nurse_sunita | staff123 | Sunita Shah | Nurse |
| pharmacist_raj | staff123 | Raj Malhotra | Pharmacist |
| accountant_preeti | staff123 | Preeti Agarwal | Accountant |

### Patients
| Username | Password | Name | Age | Blood Group |
|----------|----------|------|-----|-------------|
| patient_rahul | patient123 | Rahul Sharma | 39 | O+ |
| patient_neha | patient123 | Neha Gupta | 35 | A+ |
| patient_arjun | patient123 | Arjun Patel | 50 | B+ |
| patient_priya | patient123 | Priya Reddy | 31 | AB+ |
| patient_vikram | patient123 | Vikram Kumar | 45 | O- |
| patient_ananya | patient123 | Ananya Iyer | 37 | A- |
| patient_suresh | patient123 | Suresh Nair | 55 | B- |
| patient_meera | patient123 | Meera Joshi | 34 | O+ |
| patient_aditya | patient123 | Aditya Desai | 42 | A+ |
| patient_kavita | patient123 | Kavita Singh | 39 | B+ |

## User Flows

### Admin Flow
1. Login with admin credentials
2. Access admin dashboard with statistics
3. Manage departments, doctors, staff, patients
4. View all appointments and records

### Doctor Flow
1. Login with doctor credentials
2. View dashboard with today's appointments
3. View upcoming appointments
4. Create medical records after completing appointments
5. Update appointment status

### Patient Flow
1. Login or register as new patient
2. View dashboard with upcoming appointments
3. Book new appointments (select doctor, date, time)
4. View medical history and records
5. Update profile information

### Staff Flow
1. Login with staff credentials
2. View dashboard with all appointments
3. Add new patients to system
4. Book appointments for patients
5. Confirm or cancel appointments
6. View patient records

## Appointment Status Workflow

```
Pending -> Confirmed -> Completed (Medical Record created)
   |
   -> Cancelled (with notes)
```

## Database Models

| Model | Description |
|-------|-------------|
| UserProfile | Extended user with role (admin/doctor/patient/staff) |
| Department | Hospital departments (Cardiology, Neurology, etc.) |
| Doctor | Doctor profiles with specialization and fees |
| DoctorSchedule | Doctor availability by day and time |
| Patient | Patient profiles with medical info |
| Staff | Staff/receptionist profiles |
| Appointment | Booking system linking patient and doctor |
| MedicalRecord | Patient medical history with vitals |

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Home page with statistics |
| `/accounts/login/` | User login |
| `/accounts/register/` | Patient self-registration |
| `/dashboard/` | Role-based dashboard redirect |
| `/admin/dashboard/` | Admin dashboard |
| `/doctor/dashboard/` | Doctor dashboard |
| `/patient/dashboard/` | Patient dashboard |
| `/staff/dashboard/` | Staff dashboard |
| `/patients/` | Patient list (admin/staff/doctor) |
| `/doctors/` | Doctor list (all users) |
| `/appointments/` | Appointment list |
| `/medical-records/` | Medical records list |
| `/admin/` | Django admin panel |

## Technologies

- **Backend**: Django 5.x
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Database**: SQLite (default)
- **Icons**: Bootstrap Icons

## File Structure

```
hospital_management/
├── hospital/                    # Main Django app
│   ├── models.py                # Database models
│   ├── views.py                 # Business logic
│   ├── forms.py                 # Form definitions
│   ├── admin.py                 # Django admin configuration
│   ├── urls.py                  # URL routing
│   └── templates/               # HTML templates
├── templates/                   # Global templates
├── hospital_management/           # Project settings
├── populate_db_indian.py         # Database population script (Indian names)
├── manage.py                    # Django management
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

## Default Passwords

When users are created through the system:
- **Patients**: patient123
- **Doctors**: doctor123
- **Staff**: staff123

## Common Commands

```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Populate database with Indian names test data
python populate_db_indian.py

# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Check for errors
python manage.py check
```

## Troubleshooting

1. **CSRF errors on login**: Make sure cookies are enabled in browser
2. **Static files not loading**: Run `python manage.py collectstatic` (if DEBUG=False)
3. **Permission denied**: Check user role in UserProfile
4. **Cannot book appointment**: Ensure doctor has schedule set up
5. **Database locked**: Stop server and delete db.sqlite3, then re-run migrations

## Security Notes

- Change default passwords before production use
- Set `DEBUG = False` in production
- Generate new `SECRET_KEY` for production
- Use HTTPS in production
- Regularly backup the database file (db.sqlite3)

## License

This is a mini-project for educational purposes.

---

For questions or issues, please refer to the project documentation or contact the developer.
