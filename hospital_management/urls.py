"""
URL configuration for hospital_management project.
"""

from django.contrib import admin
from django.urls import path, include
from hospital import views as hospital_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("hospital.urls")),
    path("accounts/", include("django.contrib.auth.urls")),  # Built-in auth URLs
    path("accounts/register/", hospital_views.register_patient, name="register"),
]
