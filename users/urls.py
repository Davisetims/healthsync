from django.urls import path
from users.views import index, login_view, patient_dashboard ,doctor_dashboard, admin_dashboard

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('patient/dashboard/', patient_dashboard, name='patient-dashboard'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor-dashboard'),
    path('superuser/dashboard/', admin_dashboard, name='admin-dashboard'),
   
]