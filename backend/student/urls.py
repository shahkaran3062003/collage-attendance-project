from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.registerStudent),
    path('', views.home),
]
