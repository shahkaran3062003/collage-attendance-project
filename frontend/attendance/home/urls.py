from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('run/', views.run, name="run"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('404/', views.notFound, name="404"),
]
