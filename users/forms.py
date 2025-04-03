from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Reminder, VirtualMeeting
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
    

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['user', 'reminder_type', 'message', 'scheduled_time']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReminderForm, self).__init__(*args, **kwargs)
        # Limit users to only patients
        self.fields['user'].queryset = User.objects.filter(user_type='patient')


class VirtualMeetingForm(forms.ModelForm):
    class Meta:
        model = VirtualMeeting
        fields = ['patient', 'meeting_time', 'meeting_link']
        widgets = {
            'meeting_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'national_id', 'country', 'city', 'plan']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            }