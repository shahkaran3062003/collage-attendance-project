
from django.shortcuts import redirect, render
from json import dumps
import requests
from json import loads

# Create your views here.


def teacher(request):
    context = {}
    teacherDetails = {}
    teacherDetails['isTeacherPanelOpen'] = 'false'
    context['name'] = ""
    if request.method == 'POST':
        id = request.POST.get('teacherId')

        if id:
            teacherDetails['isTeacherPanelOpen'] = 'true'
            teacherDetails['tid'] = id
            context['name'] = "karan shah"
            teacherDetails['name'] = "karan shah"
            teacherDetails['address'] = "vadodara"
            teacherDetails['mobile'] = "7043203802"
            teacherDetails['email'] = "shahkaran3062003@gmail.com"
    print(teacherDetails)
    teacherDetails = dumps(teacherDetails)
    context['teacherDetails'] = teacherDetails
    return render(request, 'teacher/home.html', context)


def register(request):
    ENDPOINT = "http://127.0.0.1:8000/teacher/register/"
    context = {}
    registerDetails = {}

    if request.method == 'POST':
        teacherData = {}
        teacherData['name'] = request.POST['name']
        teacherData['address'] = request.POST['address']
        teacherData['contact'] = request.POST['mobile']
        teacherData['email'] = request.POST['email']
        teacherData['department'] = request.POST['department']

        try:
            teacherData['img'] = request.POST['userImage'].split(";base64,")[1]
        except Exception:
            registerDetails['isError'] = 'true'
            registerDetails = dumps(registerDetails)
            context['registerDetails'] = registerDetails
            context['errorMess'] = "Please Click image."
            return render(request, "teacher/register.html", context)

        response = requests.get(ENDPOINT, json={"data": teacherData})
        if (response):
            registerDetails = loads(response.text)
            if (registerDetails['isError'] == 'success'):
                registerDetails['isError'] = 'true'
                context['success'] = True
            context['errorMess'] = registerDetails['errorMess']
            context['registerDetails'] = dumps(registerDetails)
            return render(request, "teacher/register.html", context)

    registerDetails['isError'] = 'false'
    registerDetails = dumps(registerDetails)
    context['registerDetails'] = registerDetails
    context['errorMess'] = "Nothing."
    return render(request, "teacher/register.html", context=context)
