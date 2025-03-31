from django.db import models
from health_profile.models import HealthProfile
from users.models import User


class MedicalHistory(models.Model):
    profile = models.ForeignKey(
            HealthProfile, 
            on_delete=models.CASCADE, 
            related_name="medical_history",
            null= True, blank=True

    )
    condition = models.CharField(max_length=255, null=True, blank=True)
    diagnosis_date = models.DateField(blank=True,null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.condition}"

class Prescription(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name="medications",
        null=True, blank=True
        )
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    prescribed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.patient.username} - {self.name}"
