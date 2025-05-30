# forum/urls.py

from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
    path('like_question/<int:pk>/', views.like_question, name='like_question'),
    path('like_comment/<int:pk>/', views.like_comment, name='like_comment'),
    path('<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('question/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),

]
