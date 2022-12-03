from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Student
from json import loads
import base64
from django.core.files import File
# Create your views here.


def registerStudent(request, *args, **kwargs):
    data = request.body
    if data:
        try:
            data = loads(data)
            data = data['data']
            filterStudent = Student.objects.filter(
                department=data['department'], year=data['year'], rollNumber=data['rollNumber'])

            if (filterStudent):
                return JsonResponse({'isError': 'true', 'errorMess': 'Roll Number Alrady Exist.'})

            with open("temp.jpg", "wb") as file:
                file.write(base64.b64decode(data['img']))

            with open("temp.jpg", 'rb') as file:
                data['img'] = File(file)
                Student.objects.create(**data)
            return JsonResponse({'isError': 'success', 'errorMess': 'New Student Register Successfully.'})

        except Exception as e:
            return JsonResponse({'isError': 'true', 'errorMess': 'server Error.'})
    return HttpResponse("working")


def home(request):
    data = Student.objects.all()
    check = Student.objects.filter(
        department='BCA', year="FY", rollNumber="20bca163")
    print(check[0])
    if (data):
        context = {}

        for i in data:
            temp = {}
            temp['name'] = i.name
            temp['rollNumber'] = i.rollNumber
            temp['address'] = i.address
            temp['contact'] = i.contact
            temp['email'] = i.email
            temp['department'] = i.department
            temp['year'] = i.year
            temp['img'] = i.img.url
            context[f"{i.id}"] = temp
        context['check'] = len(check)
    return JsonResponse(context)
