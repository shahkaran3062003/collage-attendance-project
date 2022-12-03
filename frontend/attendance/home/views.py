from typing import ContextManager
from django.shortcuts import redirect, render
from json import dumps
from django.http import HttpResponseRedirect

STATE = False


def get_barchart_data(year):
    days = [
        year, [10, 20, 30, 40, 10, 20, 30, 40, 10, 20]
    ]
    days = dumps(days)
    return days


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['password_confirmation']
        terms = request.POST.getlist("accept_terms")

    return render(request, "home/register.html")


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

    return render(request, "home/login.html")


def home(request):
    # if not(request.user.is_authenticated):
    #     return redirect("login/")
    global STATE
    context = {"state": "Running" if STATE else "Start", "teachers": 50,
               "students": 150, "classes": 30, "FY": get_barchart_data("FY"), "SY": get_barchart_data("SY"), "TY": get_barchart_data("TY")}
    return render(request, "home/home.html", context)


def run(request):
    global STATE
    STATE = not STATE
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def notFound(request):
    return render(request, 'home/404.html')
