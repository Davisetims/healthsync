from django import forms
from .models import Appointment, User

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type="doctor"), 
        label="Select Doctor",
        empty_label="Choose a doctor"
    )
    
    class Meta:
        model = Appointment
        fields = ["doctor", "appointment_date", "notes"]
        widgets = {
            "appointment_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
