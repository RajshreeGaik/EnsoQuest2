# ensoquest_app/forms.py

from django import forms
from .models import Feedback
from .models import Notice

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'rating', 'expectations_met', 'improvement_suggestions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'expectations_met': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Share your thoughts...', 'rows': 3}),
            'improvement_suggestions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your suggestions...', 'rows': 3}),
        }


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']

