from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('settings', views.editProfile, name='edit_profile'),
    path('delete', views.deleteProfile, name='delete_profile'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile/<str:username>/export/', views.export_profile_submissions_excel, name='export_profile_excel'),
]