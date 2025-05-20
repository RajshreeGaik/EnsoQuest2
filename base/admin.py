from django.contrib import admin
from .models import Message, Blog
from .models import Feedback 

# Register your models here.
admin.site.register(Message)
admin.site.register(Blog)

admin.site.register(Feedback)  