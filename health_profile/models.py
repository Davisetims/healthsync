from django.db import models
from users.models import User

class HealthProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                        related_name="health_profile", null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    blood_type = models.CharField(
        max_length=5, 
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), 
                 ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), 
                 ('AB+', 'AB+'), ('AB-', 'AB-')],
                   blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Health Profile"

