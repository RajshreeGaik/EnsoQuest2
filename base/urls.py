from django.urls import path
from django.conf.urls import handler404
from . import  views
from base.views import notification_list


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
    path('blogs/create/', views.create_blog, name='create_blog'),
    path('blogs/<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),
    path('blogs/<int:blog_id>/like/', views.like_blog, name='like_blog'),
    path('comment/<int:blog_id>/', views.comment_blog, name='comment_blog'), 
    path('search/users', views.search_users_view, name='search_users'),
    path('search/', views.search_view, name='search'),  # Search without category
    path('search/<str:category>/', views.search_view, name='search_category'),  # Search with category
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/add/', views.add_notice, name='add_notice'),
    path('notices/edit/<int:pk>/', views.edit_notice, name='edit_notice'),
    path('upload/', views.upload_resource, name='upload_resource'),
    path('resources/', views.resources_view, name='resource_list'),

    path('feedback/', views.feedback_dashboard, name='feedback_dashboard'),
    path('feedback/create/', views.create_feedback_form, name='create_feedback_form'),
    path('feedback/fill/<int:form_id>/', views.feedback_fill_form, name='fill_feedback_form'),
    path('feedback/responses/<int:form_id>/', views.view_feedback_responses, name='view_feedback_responses'),
    path('notifications/', notification_list, name='notifications'),
    

]







