from django.urls import path
from . import  views

urlpatterns =[
    path('', views.home, name='home'),
    path('leaderboard', views.leaderboard_view, name='leaderboard'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('resources', views.resources_view, name='resources'),
    path('about', views.about_view, name='about'),
    path('contact', views.contact_view, name='contact'),
    path('terms_conditions', views.terms_conditions_view, name='terms_conditions'),
    path('blogs', views.blogs_view, name='blogs'),
    path('blogs/<str:blog_id>', views.blog_view, name='blog')
]