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
    


RATING_CHOICES = [
    (1, '1 - Poor'),
    (2, '2 - Fair'),
    (3, '3 - Good'),
    (4, '4 - Very Good'),
    (5, '5 - Excellent'),
]

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    expectations_met = models.TextField()
    improvement_suggestions = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

