from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.db.models import Q, Count
from datetime import datetime, date, timedelta
from .models import (
    UserProfile,
    Department,
    Doctor,
    DoctorSchedule,
    Patient,
    Staff,
    Appointment,
    MedicalRecord,
)
from .forms import (
    PatientRegistrationForm,
    PatientForm,
    PatientUpdateForm,
    DoctorForm,
    DoctorUpdateForm,
    DoctorScheduleForm,
    StaffForm,
    StaffUpdateForm,
    AppointmentForm,
    AppointmentStatusForm,
    MedicalRecordForm,
)


# ============== ROLE CHECK HELPERS ==============


def is_admin(user):
    return hasattr(user, "profile") and user.profile.role == "admin"


def is_doctor(user):
    return hasattr(user, "profile") and user.profile.role == "doctor"


def is_patient(user):
    return hasattr(user, "profile") and user.profile.role == "patient"


def is_staff_member(user):
    return hasattr(user, "profile") and user.profile.role == "staff"


def is_doctor_or_staff(user):
    return is_doctor(user) or is_staff_member(user)


# ============== HOME & AUTH VIEWS ==============


class HomeView(TemplateView):
    template_name = "hospital/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.filter(is_active=True)[:6]
        context["departments"] = Department.objects.all()
        context["total_doctors"] = Doctor.objects.filter(is_active=True).count()
        context["total_patients"] = Patient.objects.count()
        return context


def register_patient(request):
    """Patient self-registration view"""
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Registration successful! Welcome to our hospital."
            )
            return redirect("patient_dashboard")
    else:
        form = PatientRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    """Redirect to role-based dashboard"""
    if is_admin(request.user):
        return redirect("admin_dashboard")
    elif is_doctor(request.user):
        return redirect("doctor_dashboard")
    elif is_patient(request.user):
        return redirect("patient_dashboard")
    elif is_staff_member(request.user):
        return redirect("staff_dashboard")
    return redirect("home")


# ============== ADMIN DASHBOARD ==============


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    today = date.today()

    context = {
        "total_patients": Patient.objects.count(),
        "total_doctors": Doctor.objects.filter(is_active=True).count(),
        "total_staff": Staff.objects.filter(is_active=True).count(),
        "total_appointments_today": Appointment.objects.filter(
            appointment_date=today
        ).count(),
        "pending_appointments": Appointment.objects.filter(status="pending").count(),
        "recent_appointments": Appointment.objects.select_related(
            "patient", "doctor"
        ).order_by("-created_at")[:10],
        "departments": Department.objects.annotate(doctor_count=Count("doctors")),
    }
    return render(request, "hospital/dashboard/admin.html", context)


# ============== DOCTOR DASHBOARD ==============


@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    """Doctor dashboard with today's appointments"""
    doctor = request.user.doctor_profile
    today = date.today()

    context = {
        "doctor": doctor,
        "today_appointments": Appointment.objects.filter(
            doctor=doctor, appointment_date=today
        )
        .select_related("patient")
        .order_by("appointment_time"),
        "upcoming_appointments": Appointment.objects.filter(
            doctor=doctor,
            appointment_date__gt=today,
            status__in=["pending", "confirmed"],
        )
        .select_related("patient")
        .order_by("appointment_date", "appointment_time")[:10],
        "total_patients_seen": Appointment.objects.filter(
            doctor=doctor, status="completed"
        )
        .values("patient")
        .distinct()
        .count(),
        "pending_appointments": Appointment.objects.filter(
            doctor=doctor, status="pending"
        ).count(),
    }
    return render(request, "hospital/dashboard/doctor.html", context)


# ============== PATIENT DASHBOARD ==============


@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    """Patient dashboard with appointments and medical history"""
    patient = request.user.patient_profile
    today = date.today()

    context = {
        "patient": patient,
        "upcoming_appointments": Appointment.objects.filter(
            patient=patient,
            appointment_date__gte=today,
            status__in=["pending", "confirmed"],
        )
        .select_related("doctor")
        .order_by("appointment_date", "appointment_time"),
        "past_appointments": Appointment.objects.filter(
            patient=patient, status="completed"
        )
        .select_related("doctor")
        .order_by("-appointment_date")[:5],
        "medical_records": MedicalRecord.objects.filter(patient=patient)
        .select_related("doctor")
        .order_by("-created_at")[:5],
        "total_appointments": Appointment.objects.filter(patient=patient).count(),
    }
    return render(request, "hospital/dashboard/patient.html", context)


# ============== STAFF DASHBOARD ==============


@login_required
@user_passes_test(is_staff_member)
def staff_dashboard(request):
    """Staff dashboard with all appointments and quick actions"""
    today = date.today()

    context = {
        "today_appointments": Appointment.objects.filter(appointment_date=today)
        .select_related("patient", "doctor")
        .order_by("appointment_time"),
        "pending_appointments": Appointment.objects.filter(status="pending")
        .select_related("patient", "doctor")
        .order_by("-created_at")[:10],
        "recent_patients": Patient.objects.select_related("user").order_by(
            "-created_at"
        )[:5],
        "total_today": Appointment.objects.filter(appointment_date=today).count(),
    }
    return render(request, "hospital/dashboard/staff.html", context)


# ============== PATIENT VIEWS ==============


class PatientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Patient
    template_name = "hospital/patients/list.html"
    context_object_name = "patients"
    paginate_by = 10

    def test_func(self):
        return (
            is_admin(self.request.user)
            or is_staff_member(self.request.user)
            or is_doctor(self.request.user)
        )

    def get_queryset(self):
        queryset = Patient.objects.select_related("user").all()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(user__username__icontains=search)
                | Q(emergency_contact_phone__icontains=search)
            )
        return queryset


class PatientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Patient
    template_name = "hospital/patients/detail.html"
    context_object_name = "patient"

    def test_func(self):
        user = self.request.user
        patient = self.get_object()
        # Admin, staff, doctors can view any patient; patients can only view their own
        return (
            is_admin(user)
            or is_staff_member(user)
            or is_doctor(user)
            or (is_patient(user) and patient.user == user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        context["appointments"] = (
            Appointment.objects.filter(patient=patient)
            .select_related("doctor")
            .order_by("-appointment_date")[:10]
        )
        context["medical_records"] = (
            MedicalRecord.objects.filter(patient=patient)
            .select_related("doctor")
            .order_by("-created_at")[:10]
        )
        return context


class PatientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "hospital/patients/form.html"
    success_url = reverse_lazy("patient_list")

    def test_func(self):
        return is_admin(self.request.user) or is_staff_member(self.request.user)

    def form_valid(self, form):
        # Create user first
        user = User.objects.create_user(
            username=form.cleaned_data["username"]
            if "username" in form.cleaned_data
            else form.cleaned_data["email"],
            email=form.cleaned_data["email"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            password="patient123",  # Default password
        )
        user.profile.role = "patient"
        user.profile.save()

        form.instance.user = user
        messages.success(
            self.request, "Patient created successfully! Default password: patient123"
        )
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Patient
    template_name = "hospital/patients/form.html"

    def get_form_class(self):
        # Patients can only update their own limited profile
        if (
            is_patient(self.request.user)
            and self.get_object().user == self.request.user
        ):
            return PatientUpdateForm
        return PatientForm

    def test_func(self):
        user = self.request.user
        patient = self.get_object()
        return (
            is_admin(user)
            or is_staff_member(user)
            or (is_patient(user) and patient.user == user)
        )

    def get_success_url(self):
        return reverse_lazy("patient_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Patient updated successfully!")
        return super().form_valid(form)


# ============== DOCTOR VIEWS ==============


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = "hospital/doctors/list.html"
    context_object_name = "doctors"

    def get_queryset(self):
        return Doctor.objects.filter(is_active=True).select_related(
            "user", "department"
        )


class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = "hospital/doctors/detail.html"
    context_object_name = "doctor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()
        context["schedules"] = DoctorSchedule.objects.filter(
            doctor=doctor, is_available=True
        )
        return context


class DoctorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "hospital/doctors/form.html"
    success_url = reverse_lazy("doctor_list")

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            password="doctor123",
        )
        user.profile.role = "doctor"
        user.profile.save()

        form.instance.user = user
        messages.success(
            self.request, "Doctor created successfully! Default password: doctor123"
        )
        return super().form_valid(form)


class DoctorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Doctor
    form_class = DoctorUpdateForm
    template_name = "hospital/doctors/form.html"

    def test_func(self):
        user = self.request.user
        doctor = self.get_object()
        return is_admin(user) or (is_doctor(user) and doctor.user == user)

    def get_success_url(self):
        return reverse_lazy("doctor_detail", kwargs={"pk": self.object.pk})


class DoctorScheduleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DoctorSchedule
    form_class = DoctorScheduleForm
    template_name = "hospital/doctors/schedule_form.html"

    def test_func(self):
        return is_admin(self.request.user) or is_doctor(self.request.user)

    def form_valid(self, form):
        doctor = get_object_or_404(Doctor, pk=self.kwargs["doctor_pk"])
        form.instance.doctor = doctor
        messages.success(self.request, "Schedule added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("doctor_detail", kwargs={"pk": self.kwargs["doctor_pk"]})


# ============== STAFF VIEWS ==============


class StaffListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Staff
    template_name = "hospital/staff/list.html"
    context_object_name = "staff_members"

    def test_func(self):
        return is_admin(self.request.user)

    def get_queryset(self):
        return Staff.objects.filter(is_active=True).select_related("user", "department")


class StaffCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = "hospital/staff/form.html"
    success_url = reverse_lazy("staff_list")

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            password="staff123",
        )
        user.profile.role = "staff"
        user.profile.save()

        form.instance.user = user
        messages.success(
            self.request,
            "Staff member created successfully! Default password: staff123",
        )
        return super().form_valid(form)


# ============== APPOINTMENT VIEWS ==============


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "hospital/appointments/list.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        if is_admin(user) or is_staff_member(user):
            queryset = Appointment.objects.select_related("patient", "doctor")
        elif is_doctor(user):
            queryset = Appointment.objects.filter(
                doctor=user.doctor_profile
            ).select_related("patient")
        elif is_patient(user):
            queryset = Appointment.objects.filter(
                patient=user.patient_profile
            ).select_related("doctor")
        else:
            queryset = Appointment.objects.none()

        # Filter by status if provided
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by("-appointment_date", "-appointment_time")


class AppointmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "hospital/appointments/book.html"

    def test_func(self):
        return is_patient(self.request.user) or is_staff_member(self.request.user)

    def form_valid(self, form):
        form.instance.scheduled_by = self.request.user

        # If patient is booking for themselves
        if is_patient(self.request.user):
            form.instance.patient = self.request.user.patient_profile

        messages.success(self.request, "Appointment booked successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        if is_patient(self.request.user):
            return reverse_lazy("patient_dashboard")
        return reverse_lazy("appointment_list")


@login_required
@user_passes_test(lambda u: is_staff_member(u) or is_patient(u))
def appointment_book_for_patient(request, patient_pk):
    """Staff booking appointment for a specific patient"""
    patient = get_object_or_404(Patient, pk=patient_pk)

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.scheduled_by = request.user
            appointment.save()
            messages.success(request, f"Appointment booked for {patient} successfully!")
            return redirect("patient_detail", pk=patient.pk)
    else:
        form = AppointmentForm()

    return render(
        request,
        "hospital/appointments/book.html",
        {"form": form, "patient": patient, "booking_for": "staff"},
    )


class AppointmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Appointment
    template_name = "hospital/appointments/detail.html"
    context_object_name = "appointment"

    def test_func(self):
        user = self.request.user
        appointment = self.get_object()

        if is_admin(user) or is_staff_member(user):
            return True
        if is_doctor(user) and appointment.doctor.user == user:
            return True
        if is_patient(user) and appointment.patient.user == user:
            return True
        return False


@login_required
@user_passes_test(is_doctor_or_staff)
def appointment_update_status(request, pk):
    """Update appointment status"""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == "POST":
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment status updated!")
            return redirect("appointment_detail", pk=appointment.pk)
    else:
        form = AppointmentStatusForm(instance=appointment)

    return render(
        request,
        "hospital/appointments/status_form.html",
        {"form": form, "appointment": appointment},
    )


# ============== MEDICAL RECORD VIEWS ==============


class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = "hospital/medical_records/list.html"
    context_object_name = "records"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        if is_admin(user) or is_staff_member(user):
            queryset = MedicalRecord.objects.select_related("patient", "doctor")
        elif is_doctor(user):
            queryset = MedicalRecord.objects.filter(
                doctor=user.doctor_profile
            ).select_related("patient")
        elif is_patient(user):
            queryset = MedicalRecord.objects.filter(
                patient=user.patient_profile
            ).select_related("doctor")
        else:
            queryset = MedicalRecord.objects.none()

        return queryset.order_by("-created_at")


class MedicalRecordDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MedicalRecord
    template_name = "hospital/medical_records/detail.html"
    context_object_name = "record"

    def test_func(self):
        user = self.request.user
        record = self.get_object()

        if is_admin(user) or is_staff_member(user):
            return True
        if is_doctor(user) and record.doctor.user == user:
            return True
        if is_patient(user) and record.patient.user == user:
            return True
        return False


class MedicalRecordCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = "hospital/medical_records/form.html"

    def test_func(self):
        return is_doctor(self.request.user)

    def get_initial(self):
        initial = super().get_initial()
        appointment = get_object_or_404(Appointment, pk=self.kwargs["appointment_pk"])
        initial["diagnosis"] = appointment.symptoms
        return initial

    def form_valid(self, form):
        appointment = get_object_or_404(Appointment, pk=self.kwargs["appointment_pk"])
        form.instance.appointment = appointment
        form.instance.patient = appointment.patient
        form.instance.doctor = self.request.user.doctor_profile

        # Update appointment status to completed
        appointment.status = "completed"
        appointment.save()

        messages.success(self.request, "Medical record created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("medical_record_detail", kwargs={"pk": self.object.pk})


# ============== DEPARTMENT VIEWS ==============


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = "hospital/departments/list.html"
    context_object_name = "departments"


class DepartmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Department
    template_name = "hospital/departments/form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("department_list")

    def test_func(self):
        return is_admin(self.request.user)
