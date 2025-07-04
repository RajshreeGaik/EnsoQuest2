from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True,verbose_name='User Object')
    #email_address = models.CharField(max_length=55,unique=True,null=True,)
    position = models.CharField(max_length=100,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    profile_img = models.ImageField(upload_to='profile_image', default='user.png',blank=True,null=True,verbose_name= 'Profile Pic')

    def __str__(self):
        return self.user.username
  
    @property
    def full_name(self):
      full_name = f"{self.user.first_name} {self.user.last_name}".strip()
      return full_name if full_name else None


