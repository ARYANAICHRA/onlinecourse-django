from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='index'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('enroll/', views.enroll, name='enroll'),
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]
