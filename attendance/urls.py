from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/create/', views.create_session, name='create_session'),
    path('sessions/<int:session_id>/mark/', views.mark_attendance, name='mark_attendance'),
    path('report/<int:session_id>/', views.attendance_report_session, name='attendance_report_session'),
    path('student-report/', views.student_attendance_report, name='student_attendance_report'),
    path('student-session-report/<int:session_id>/', views.student_session_report, name='student_session_report'),
    path('export-excel/<int:session_id>/', views.export_attendance_excel, name='export_excel'),
]
