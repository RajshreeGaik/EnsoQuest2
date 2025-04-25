from django.urls import path
from . import views

urlpatterns =[
    path('all_quiz/',views.all_quize_view, name='all_quiz'),
    path('search/<str:category>/',views.search_view, name='search'),
]