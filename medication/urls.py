from django.urls import path
from medication.views import get_medical_records

urlpatterns = [
    path('get/medical/records/', get_medical_records, name='get-medical-records'),
    
   
]