# quiz/forms.py
from django import forms
from .models import Quiz

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category', 'quiz_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
