from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class PatientRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "national_id", "country", "city", "plan", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "patient"  # Set user type to patient
        if commit:
            user.save()
        return user
