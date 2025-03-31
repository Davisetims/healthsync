from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    FREE = 'free'
    PREMIUM = 'premium'
    PLAN_CHOICES = [(FREE, 'Free'), (PREMIUM, 'Premium')]

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
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username

