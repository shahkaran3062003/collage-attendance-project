
from django.shortcuts import redirect, render
from json import dumps

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
    return render(request, 'teacher/register.html')
