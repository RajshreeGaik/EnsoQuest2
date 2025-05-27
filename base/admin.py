from django.contrib import admin
from .models import Message, Blog
from .models import Feedback 
from .models import Notice
from .models import Resource

# Register your models here.
admin.site.register(Message)
admin.site.register(Blog)
admin.site.register(Feedback) 
admin.site.register(Notice)
admin.site.register(Resource)