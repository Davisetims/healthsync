from django.contrib import admin
from medication.models import MedicalHistory, Prescription

admin.site.register(MedicalHistory)
admin.site.register(Prescription)


