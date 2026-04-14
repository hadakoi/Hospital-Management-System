from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
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


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_role",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "profile__role")

    def get_role(self, obj):
        return obj.profile.role

    get_role.short_description = "Role"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


class DoctorScheduleInline(admin.TabularInline):
    model = DoctorSchedule
    extra = 1


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "get_full_name",
        "department",
        "specialization",
        "experience_years",
        "consultation_fee",
        "is_active",
    )
    list_filter = ("department", "is_active", "experience_years")
    search_fields = (
        "user__first_name",
        "user__last_name",
        "specialization",
        "qualification",
    )
    inlines = [DoctorScheduleInline]

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = "Name"


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "doctor",
        "get_day_of_week_display",
        "start_time",
        "end_time",
        "is_available",
    )
    list_filter = ("day_of_week", "is_available", "doctor")
    search_fields = ("doctor__user__first_name", "doctor__user__last_name")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "get_full_name",
        "gender",
        "blood_group",
        "get_age",
        "emergency_contact_phone",
    )
    list_filter = ("gender", "blood_group")
    search_fields = ("user__first_name", "user__last_name", "emergency_contact_name")

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    get_full_name.short_description = "Name"

    def get_age(self, obj):
        return obj.get_age()

    get_age.short_description = "Age"


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("get_full_name", "designation", "department", "is_active")
    list_filter = ("designation", "is_active", "department")
    search_fields = ("user__first_name", "user__last_name")

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    get_full_name.short_description = "Name"


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "appointment_date",
        "appointment_time",
        "status",
        "created_at",
    )
    list_filter = ("status", "appointment_date", "doctor")
    search_fields = (
        "patient__user__first_name",
        "patient__user__last_name",
        "doctor__user__first_name",
    )
    date_hierarchy = "appointment_date"

    fieldsets = (
        (
            "Appointment Details",
            {"fields": ("patient", "doctor", "appointment_date", "appointment_time")},
        ),
        ("Status", {"fields": ("status", "cancellation_notes")}),
        ("Additional Info", {"fields": ("symptoms", "notes", "scheduled_by")}),
    )


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "created_at", "follow_up_date")
    list_filter = ("created_at", "doctor")
    search_fields = (
        "patient__user__first_name",
        "patient__user__last_name",
        "diagnosis",
    )
    date_hierarchy = "created_at"

    fieldsets = (
        ("Patient & Doctor", {"fields": ("patient", "doctor", "appointment")}),
        (
            "Medical Information",
            {"fields": ("diagnosis", "symptoms", "prescription", "notes")},
        ),
        (
            "Vitals",
            {"fields": ("blood_pressure", "temperature", "weight", "heart_rate")},
        ),
        ("Follow-up", {"fields": ("follow_up_date",)}),
    )
