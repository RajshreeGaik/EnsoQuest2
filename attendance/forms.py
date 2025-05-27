from django import forms
from .models import Session, Attendance
from django.contrib.auth.models import User

class SessionForm(forms.ModelForm):
    trainees = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=False),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Session
        fields = ['name', 'description', 'trainees']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['present']
