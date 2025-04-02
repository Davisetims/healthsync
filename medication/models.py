from django.db import models
from health_profile.models import HealthProfile
from users.models import User


class MedicalRecord(models.Model):
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
        null=True, blank=True,
        limit_choices_to={'user_type': 'patient'}
        )
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    prescribed_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'doctor'},
        blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.username} - {self.name}"



class MedicalTest(models.Model):
    medical_record = models.ForeignKey(
        MedicalRecord, on_delete=models.CASCADE,
        null=True, blank= True
        )
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name="medical_tests",
        limit_choices_to={'user_type': 'patient'}
        )
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE,
          related_name="conducted_tests",
          limit_choices_to={'user_type': 'doctor'}
          )
    test_name = models.CharField(max_length=255)
    test_date = models.DateTimeField()
    results = models.JSONField(null=True, blank=True)

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed")
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.username} - {self.test_name}"
