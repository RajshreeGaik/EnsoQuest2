# ensoquest_app/forms.py

from django import forms
from .models import Notice
from .models import Resource
from .models import Blog
from ckeditor.widgets import CKEditorWidget
from .models import Comment

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'author_name']


  
class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = ['title', 'content', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


