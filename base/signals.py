# base/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from base.models import Notification
from base.models import Resource, Blog,  Notice, FeedbackForm
from forum.models import  Question 
from quiz.models import Quiz
from django.core.mail import send_mass_mail



# adjust app name

def notify_all_users(message, url=None, category=None):
    users = User.objects.filter(is_active=True).only('id', 'email')

    # Bulk notification creation
    notifications = [
        Notification(user=user, message=message, url=url, category=category)
        for user in users
    ]
    Notification.objects.bulk_create(notifications)

    # Optional: Send all emails in one go
    email_tuples = [
        (
            'LMS Notification',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        for user in users if user.email
    ]
    send_mass_mail(email_tuples, fail_silently=True)

# Feedback
@receiver(post_save, sender=FeedbackForm)
def feedback_notification(sender, instance, created, **kwargs):
    msg = f"Feedback '{instance.title}' was updated."
    notify_all_users(msg, url=f"/feedback/{instance.id}/", category='feedbackform')

# Resource
@receiver(post_save, sender=Resource)
def resource_notification(sender, instance, created, **kwargs):
    msg = f"Resource '{instance.title}' was updated."
    notify_all_users(msg, url=f"/resource/{instance.id}/", category='resource')

# Test
@receiver(post_save, sender=Quiz)
def test_notification(sender, instance, created, **kwargs):
    msg = f"Test '{instance.title}' was updated."
    notify_all_users(msg, url=f"/test/{instance.id}/", category='quiz')

# Blog
@receiver(post_save, sender=Blog)
def blog_notification(sender, instance, created, **kwargs):
    msg = f"Blog '{instance.title}' was updated."
    notify_all_users(msg, url=f"/blog/{instance.id}/", category='blog')

# Forum
@receiver(post_save, sender=Question)
def forum_notification(sender, instance, created, **kwargs):
    msg = f"Forum '{instance.title}' was updated."
    notify_all_users(msg, url=f"/forum/{instance.id}/", category='forum')

# Notice
@receiver(post_save, sender=Notice)
def notice_notification(sender, instance, created, **kwargs):
    msg = f"Notice '{instance.title}' was updated."
    notify_all_users(msg, url=f"/notice/{instance.id}/", category='notice')
