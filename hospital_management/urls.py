from django.contrib import admin
from django.urls import path, include
from hospital import views as hospital_views

urlpatterns = [
    # Custom admin dashboard must come BEFORE Django admin
    path("admin/dashboard/", hospital_views.admin_dashboard, name="admin_dashboard"),
    path("admin/", admin.site.urls),
    path("", include("hospital.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", hospital_views.register_patient, name="register"),
]
