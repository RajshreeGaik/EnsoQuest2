from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resource, name='upload_resource'),
    path('resources/', views.resource_list, name='resource_list'),
]


