from django.urls import path

from . import views

urlpatterns = [
    path('', views.student, name="student"),
    path('register/', views.register, name="student_register"),
    path('attendance/<str:year>', views.attendance, name="attendance"),

]
