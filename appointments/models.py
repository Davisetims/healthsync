from django.db import models
from users.models import User


STATUS = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancel', 'Cancelled'),
        
    ]
class Appointment(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name="patient_appointments", 
        null=True, blank=True,
        limit_choices_to={'user_type': 'patient'})
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name="doctor_appointments", 
        limit_choices_to={'user_type': 'doctor'})
    status = models.CharField(
        choices=STATUS, 
        default='scheduled', 
        null=True, blank=True, 
        max_length=10)
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.username} ({self.appointment_date})"
