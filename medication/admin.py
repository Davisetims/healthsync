from django.contrib import admin
from medication.models import MedicalRecord, Prescription, MedicalTest

admin.site.register(MedicalTest)
admin.site.register(MedicalRecord)
admin.site.register(Prescription)


