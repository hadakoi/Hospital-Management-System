from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TimeInput):
    input_type = "time"


# ============== USER FORMS ==============


class PatientRegistrationForm(UserCreationForm):
    """Form for patient self-registration"""

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Update profile
            user.profile.role = "patient"
            user.profile.phone = self.cleaned_data["phone"]
            user.profile.address = self.cleaned_data["address"]
            user.profile.save()
            # Create patient profile
            Patient.objects.create(user=user)
        return user


class UserForm(forms.ModelForm):
    """Form for creating users (admin/staff use)"""

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserProfileForm(forms.ModelForm):
    """Form for user profile"""

    class Meta:
        model = UserProfile
        fields = ["role", "phone", "address"]


# ============== PATIENT FORMS ==============


class PatientForm(forms.ModelForm):
    """Form for creating/editing patients"""

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)

    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "gender",
            "blood_group",
            "emergency_contact_name",
            "emergency_contact_phone",
            "medical_history",
        ]
        widgets = {
            "date_of_birth": DateInput(),
            "medical_history": forms.Textarea(attrs={"rows": 4}),
        }


class PatientUpdateForm(forms.ModelForm):
    """Form for patients to update their own profile"""

    class Meta:
        model = Patient
        fields = [
            "date_of_birth",
            "gender",
            "blood_group",
            "emergency_contact_name",
            "emergency_contact_phone",
            "medical_history",
        ]
        widgets = {
            "date_of_birth": DateInput(),
            "medical_history": forms.Textarea(attrs={"rows": 4}),
        }


# ============== DOCTOR FORMS ==============


class DoctorForm(forms.ModelForm):
    """Form for creating/editing doctors"""

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)

    class Meta:
        model = Doctor
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "department",
            "specialization",
            "qualification",
            "experience_years",
            "consultation_fee",
            "is_active",
        ]


class DoctorUpdateForm(forms.ModelForm):
    """Form for updating doctor profile"""

    class Meta:
        model = Doctor
        fields = [
            "department",
            "specialization",
            "qualification",
            "experience_years",
            "consultation_fee",
        ]


class DoctorScheduleForm(forms.ModelForm):
    """Form for doctor schedules"""

    class Meta:
        model = DoctorSchedule
        fields = ["day_of_week", "start_time", "end_time", "is_available"]
        widgets = {
            "start_time": TimeInput(),
            "end_time": TimeInput(),
        }


# ============== STAFF FORMS ==============


class StaffForm(forms.ModelForm):
    """Form for creating/editing staff"""

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)

    class Meta:
        model = Staff
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "designation",
            "department",
            "is_active",
        ]


class StaffUpdateForm(forms.ModelForm):
    """Form for updating staff profile"""

    class Meta:
        model = Staff
        fields = ["designation", "department"]


# ============== APPOINTMENT FORMS ==============


class AppointmentForm(forms.ModelForm):
    """Form for booking appointments with time slot validation"""

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(is_active=True), empty_label="Select Doctor"
    )

    class Meta:
        model = Appointment
        fields = ["doctor", "appointment_date", "appointment_time", "symptoms", "notes"]
        widgets = {
            "appointment_date": DateInput(),
            "appointment_time": TimeInput(),
            "symptoms": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get("doctor")
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        if doctor and appointment_date and appointment_time:
            from datetime import datetime

            # Check if the date/time is in the future
            appointment_datetime = datetime.combine(appointment_date, appointment_time)
            if appointment_datetime <= datetime.now():
                raise forms.ValidationError(
                    "Appointment must be scheduled for a future date and time."
                )

            # Check if the doctor is available on this day
            day_of_week = appointment_date.weekday()
            schedule = DoctorSchedule.objects.filter(
                doctor=doctor,
                day_of_week=day_of_week,
                start_time__lte=appointment_time,
                end_time__gte=appointment_time,
                is_available=True,
            ).first()

            if not schedule:
                raise forms.ValidationError(
                    f"Dr. {doctor.user.get_full_name()} is not available on this date/time. "
                    f"Please check the doctor's schedule."
                )

            # Check if the slot is already booked
            existing = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=["pending", "confirmed"],
            ).exists()

            if existing:
                raise forms.ValidationError(
                    "This time slot is already booked. Please select another time."
                )

        return cleaned_data


class AppointmentStatusForm(forms.ModelForm):
    """Form for updating appointment status"""

    class Meta:
        model = Appointment
        fields = ["status", "cancellation_notes"]
        widgets = {
            "cancellation_notes": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Reason for cancellation/postponement"}
            ),
        }


# ============== MEDICAL RECORD FORMS ==============


class MedicalRecordForm(forms.ModelForm):
    """Form for creating medical records"""

    class Meta:
        model = MedicalRecord
        fields = [
            "diagnosis",
            "symptoms",
            "prescription",
            "notes",
            "blood_pressure",
            "temperature",
            "weight",
            "heart_rate",
            "follow_up_date",
        ]
        widgets = {
            "follow_up_date": DateInput(),
            "diagnosis": forms.Textarea(attrs={"rows": 3}),
            "symptoms": forms.Textarea(attrs={"rows": 3}),
            "prescription": forms.Textarea(attrs={"rows": 4}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }
