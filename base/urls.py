from django.urls import path
from django.conf.urls import handler404
from . import  views


handler404 = views.custom_404 

urlpatterns =[
    path('', views.home, name='home'),
    path('leaderboard', views.leaderboard_view, name='leaderboard'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('message/<int:id>', views.message_view, name='message'),
    path('resources', views.resources_view, name='resources'),
    path('about', views.about_view, name='about'),
    path('contact', views.contact_view, name='contact'),
    path('terms_conditions', views.terms_conditions_view, name='terms_conditions'),
    path('blogs', views.blogs_view, name='blogs'),
    path('blogs/<str:blog_id>', views.blog_view, name='blog'),
    path('search/users', views.search_users_view, name='search_users'),
    path('search/', views.search_view, name='search'),  # Search without category
    path('search/<str:category>/', views.search_view, name='search_category'),  # Search with category
    path('feedback', views.feedback_view, name='feedback'),
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/add/', views.add_notice, name='add_notice'),
    path('notices/edit/<int:pk>/', views.edit_notice, name='edit_notice'),
]




