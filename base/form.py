# ensoquest_app/forms.py

from django import forms
from .models import Notice
from .models import Resource

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file']
