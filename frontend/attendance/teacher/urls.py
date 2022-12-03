from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher, name="teacher"),
    path('register/', views.register, name="teacher_register"),

]
