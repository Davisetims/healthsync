from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    FREE = 'free'
    PREMIUM = 'premium'
    PLAN_CHOICES = [(FREE, 'Free'), (PREMIUM, 'Premium')]

    USER_TYPES = [
        ('patient', 'Chronic Illness Patient'),
        ('fitness', 'Fitness Enthusiast'),
        ('professional', 'Busy Professional'),
        ('doctor', 'Healthcare Provider'),

    ]
   

    phone_regex = RegexValidator(
    regex=r'^\+\d{1,3}\d{9}$',  
    message="Phone number must start with '+' followed by country code and 9 digits."
)


    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20,
        validators=[phone_regex],
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    national_id = models.CharField(max_length=8, blank=True, null=True)
    country =models.CharField(blank=True,null=True, max_length=50)
    city = models.CharField(blank=True, null=True, max_length=50)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default=FREE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='patient')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username


class Reminder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'},
        related_name="reminders")
    reminder_type = models.CharField(max_length=20, choices=[('medication', 'Medication'), ('appointment', 'Appointment')])
    message = models.TextField()
    scheduled_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.reminder_type} ({self.scheduled_time})"


class VirtualMeeting(models.Model):
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 'doctor'},
        related_name="shared_data")
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 'patient'},
        related_name="received_data")
    meeting_time = models.DateTimeField(null=True, blank=True)
    meeting_link = models.URLField()
    

    def __str__(self):
        return f"{self.doctor.username} → {self.patient.username}"
