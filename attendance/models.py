from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    trainees = models.ManyToManyField(User, related_name='sessions')

    def __str__(self):
        return self.name

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    trainee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('session', 'trainee', 'date')

    def __str__(self):
        return f"{self.trainee.username} - {self.session.name} - {self.date} - {'Present' if self.present else 'Absent'}"
