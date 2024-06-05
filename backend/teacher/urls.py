from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerTeacher),
    path('', views.home),
]
