from django.urls import path
from users.views import index, login_view, patient_dashboard ,\
    doctor_dashboard, admin_dashboard, logout_view, user_list,\
    register_patient, send_reminder, create_virtual_meeting, get_virtual_meetings,\
    edit_profile

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('patient/dashboard/', patient_dashboard, name='patient-dashboard'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor-dashboard'),
    path('superuser/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('patients/', user_list, name='patients-list'),
    path("signup/", register_patient, name="register-patient"),
    path('send/reminder/', send_reminder, name='send-reminder'),
    path('create/meeting/', create_virtual_meeting, name='create-virtual-meeting'),
    path('get/meeting/details/', get_virtual_meetings, name='get_virtual_meetings'),
    path('edit/profile/', edit_profile, name='edit_profile'),
   
   
]