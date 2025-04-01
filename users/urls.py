from django.urls import path
from users.views import index, login_view, patient_dashboard

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('patient/dashboard/', patient_dashboard, name='patient-dashboard'),
   
]