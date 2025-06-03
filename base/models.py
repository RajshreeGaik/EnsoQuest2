from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey('auth.user',on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username},{self.subject}"
    
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    STATUS = (
        ('public','Public'),
        ('private','Private'),
    )
    status = models.CharField(max_length=7, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class FeedbackForm(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_users = models.ManyToManyField(User, related_name='assigned_feedbacks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


QUESTION_TYPES = (
    ('MCQ', 'Multiple Choice'),
    ('PARAGRAPH', 'Paragraph'),
    ('CHECKBOX', 'Checkbox'),
    ('RATING', 'Rating'),
)

class FeedbackQuestion(models.Model):
    form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=1024)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    options = models.TextField(blank=True, help_text="Comma-separated options (for MCQ and CHECKBOX)")

    def __str__(self):
        return self.text


class FeedbackResponse(models.Model):
    form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)


class FeedbackAnswer(models.Model):
    response = models.ForeignKey(FeedbackResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(FeedbackQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)
