from django.urls import path
from . import views

urlpatterns =[
    path('all_quiz/',views.all_quiz_view, name='all_quiz'),
    path('search/<str:category>/',views.search_view, name='search'),
    path('add/', views.add_quiz_view, name='add_quiz'), 
    path('<int:quiz_id>',views.quiz_view, name='quiz'),
    path('<int:submission_id>/result',views.quiz_result_view, name='quiz_result'),
    path('<int:quiz_id>/report/', views.quiz_report_view, name='quiz_report'),
    path('<int:quiz_id>/report/export/', views.export_quiz_report_excel, name='quiz_report_export'),

]
