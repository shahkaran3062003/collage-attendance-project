
from django.shortcuts import render
from json import dumps, loads
import pandas as pd
from datetime import datetime
import requests
# Create your views here.


def student(request):
    context = {}
    context['name'] = ""
    studentDetails = {}
    studentDetails['isStudentPanelOpen'] = 'false'
    if request.method == 'POST':
        roll_number_FY = request.POST.get('Filter-FY')
        roll_number_SY = request.POST.get('rollNumber-SY')
        roll_number_TY = request.POST.get('rollNumber-TY')
        id = request.POST.get('studentId')
        if (roll_number_FY):
            print(roll_number_FY)
        elif (roll_number_SY):
            print(roll_number_SY)
        elif (roll_number_TY):
            print(roll_number_TY)

        if id:
            studentDetails['sid'] = id
            studentDetails['isStudentPanelOpen'] = 'true'
            context['name'] = "karan shah"
            studentDetails['name'] = 'karan shah'
            studentDetails['rollnumber'] = '20bca163'
            studentDetails['address'] = 'vadoara'
            studentDetails['mobile'] = '7043203802'
            studentDetails['email'] = "shahkaran3062003@gmail.com"
            studentDetails['year'] = "SY"
            studentDetails['department'] = "BCA"

    # if roll_Number:
    studentDetails = dumps(studentDetails)
    context['studentDetails'] = studentDetails
    context['department'] = "BCA"

    return render(request, "student/home.html", context)


# def convertImgToBase64(string):
#     return base64.b64decode(string.split(';base64,')[1])


def register(request):
    ENDPOINT = "http://127.0.0.1:8000/student/register/"
    context = {}
    registerDetails = {}

    if request.method == 'POST':
        studentData = {}
        studentData['name'] = request.POST['name']
        studentData['rollNumber'] = request.POST['rollNumber']
        studentData['address'] = request.POST['address']
        studentData['contact'] = request.POST['contact']
        studentData['email'] = request.POST['email']
        studentData['department'] = request.POST['department']
        studentData['year'] = request.POST['year']
        try:
            studentData['img'] = request.POST['userImage'].split(";base64,")[1]
        except Exception:
            registerDetails['isError'] = 'true'
            registerDetails = dumps(registerDetails)
            context['registerDetails'] = registerDetails
            context['errorMess'] = "Please Click image."
            return render(request, "student/register.html", context)

        response = requests.get(ENDPOINT, json={"data": studentData})
        if (response):
            registerDetails = loads(response.text)
            if (registerDetails['isError'] == 'success'):
                registerDetails['isError'] = 'true'
                context['success'] = True
            context['errorMess'] = registerDetails['errorMess']
            context['registerDetails'] = dumps(registerDetails)
            return render(request, "student/register.html", context)

    registerDetails['isError'] = 'false'
    registerDetails = dumps(registerDetails)
    context['registerDetails'] = registerDetails
    context['errorMess'] = "Nothing."
    return render(request, "student/register.html", context=context)


def attendance(request, year):

    ENDPOINT = "http://localhost:1234/attendance"
    current_month = datetime.today().strftime("%Y-%m")

    context = {}

    if request.method == 'POST':
        rollNumber = request.POST.get("RollNumber")
        current_month = request.POST.get("Filter-Month")
        print(rollNumber, current_month)

    responce = requests.get(
        ENDPOINT, params={"department": "BCA", "year": year, "month": current_month})

    print(responce.text)

    file_path = f"static/attendance/{year}/{current_month.split('-')[0]}/{current_month}.csv"
    context['year'] = "First Year" if year == "fy" else "Second Year" if year == "sy" else "Third Year"
    data = pd.read_csv(file_path).T.to_dict()
    context['Year'] = year
    context['attendace'] = data
    context['month'] = dumps(current_month)
    context['file_path'] = file_path[7:]

    return render(request, "student/attendance.html", context)
