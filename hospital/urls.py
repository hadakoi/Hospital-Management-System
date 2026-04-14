from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("patients/", views.PatientListView.as_view(), name="patient_list"),
    path("patients/add/", views.PatientCreateView.as_view(), name="patient_create"),
    path(
        "patients/<int:pk>/", views.PatientDetailView.as_view(), name="patient_detail"
    ),
    path(
        "patients/<int:pk>/edit/",
        views.PatientUpdateView.as_view(),
        name="patient_update",
    ),
    path("doctors/", views.DoctorListView.as_view(), name="doctor_list"),
    path("doctors/add/", views.DoctorCreateView.as_view(), name="doctor_create"),
    path("doctors/<int:pk>/", views.DoctorDetailView.as_view(), name="doctor_detail"),
    path(
        "doctors/<int:pk>/edit/", views.DoctorUpdateView.as_view(), name="doctor_update"
    ),
    path(
        "doctors/<int:doctor_pk>/schedule/add/",
        views.DoctorScheduleCreateView.as_view(),
        name="doctor_schedule_create",
    ),
    path("staff/", views.StaffListView.as_view(), name="staff_list"),
    path("staff/add/", views.StaffCreateView.as_view(), name="staff_create"),
    path("appointments/", views.AppointmentListView.as_view(), name="appointment_list"),
    path(
        "appointments/book/",
        views.AppointmentCreateView.as_view(),
        name="appointment_create",
    ),
    path(
        "appointments/book/<int:patient_pk>/",
        views.appointment_book_for_patient,
        name="appointment_book_for_patient",
    ),
    path(
        "appointments/<int:pk>/",
        views.AppointmentDetailView.as_view(),
        name="appointment_detail",
    ),
    path(
        "appointments/<int:pk>/status/",
        views.appointment_update_status,
        name="appointment_update_status",
    ),
    path(
        "medical-records/",
        views.MedicalRecordListView.as_view(),
        name="medical_record_list",
    ),
    path(
        "medical-records/<int:pk>/",
        views.MedicalRecordDetailView.as_view(),
        name="medical_record_detail",
    ),
    path(
        "medical-records/add/<int:appointment_pk>/",
        views.MedicalRecordCreateView.as_view(),
        name="medical_record_create",
    ),
    path("departments/", views.DepartmentListView.as_view(), name="department_list"),
    path(
        "departments/add/",
        views.DepartmentCreateView.as_view(),
        name="department_create",
    ),
]
