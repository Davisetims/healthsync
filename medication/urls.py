from django.urls import path
from medication.views import get_medical_records, post_prescription

urlpatterns = [
    path('get/medical/records/', get_medical_records, name='get-medical-records'),
    path("post/prescription/", post_prescription, name="post-prescription"),
  
   
]