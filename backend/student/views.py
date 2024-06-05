from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Student
from json import loads
import base64
from django.core.files import File

# from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
import cv2
from face_recognition import face_encodings, load_image_file, face_locations, face_distance, compare_faces
# from numpy import argmin
import numpy as np
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import os

# id = Student.objects.values('id')[0]

# encodings = Student.objects.get(id='s-1')
all_students = Student.objects.all()

allEncodings = [std.get_encodings() for std in all_students]
name = [f'{std.name}-{std.rollNumber}' for std in all_students]

# print(allEncodings)


def test_webcam():
    WIDTH, HEIGHT = 1600, 900

    cap = cv2.VideoCapture(0)
    cap.set(3, HEIGHT)
    cap.set(4, WIDTH)
    i = 0
    while True:
        _, img = cap.read()
        faceLocation = face_locations(img)

        clientEncodings = face_encodings(img, faceLocation)
        # print(type(clientEncodings))

        for encodings, faces in zip(clientEncodings, faceLocation):
            # matches = compare_faces(allEncodings, encodings)
            faceDistance = face_distance(allEncodings, encodings)
            index = np.argmin(faceDistance)
            cv2.rectangle(img, (faces[3], faces[0]),
                          (faces[1], faces[2]), (255, 0, 0), 2, cv2.FILLED)
            if (faceDistance[index] < 0.39):
                i += 1
                print(name[index], faceDistance[index])

        cv2.imshow("images", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def test_img():
    path = r"D:\bca prectice\django\collage attendance project\backend\faces\student\test"
    all_img = os.listdir(path)
    print(all_img)
    for i in all_img:
        img = cv2.imread(os.path.join(path, i))

        faceLocation = face_locations(img, number_of_times_to_upsample=2)
        print(len(faceLocation))
        clientEncodings = face_encodings(img, faceLocation)
        for encodings, faces in zip(clientEncodings, faceLocation):
            matches = compare_faces(allEncodings, encodings)
            faceDistance = face_distance(allEncodings, encodings)
            index = np.argmin(faceDistance)
            cv2.rectangle(img, (faces[3], faces[0]),
                          (faces[1], faces[2]), (255, 0, 0), 2, cv2.FILLED)

            if (faceDistance[index] < 0.53):
                # i += 1
                # if (name[index] == 'rahul-20bca100'):
                # cv2.putText(img, name[index], (faces[3], faces[2]),
                #             cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 0, 0), 5)
                print(name[index], faceDistance[index])
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.imshow("image", img)
        cv2.waitKey(0)


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
                # data['encodings'] = bytes(
                #     face_encodings(load_image_file("temp.jpg"))[0])
                encodings = face_encodings(load_image_file("temp.jpg"))
                encodings = encodings[0].tolist()
                # print(encodings)
                # encodings = list[encodings[0]]
                # print(encodings)
                # print(data)
                # print(len(encodings))
                obj = Student.objects.create(**data)
                obj.set_encodings(encodings)
                obj.save()
            return JsonResponse({'isError': 'success', 'errorMess': 'New Student Register Successfully.'})

        except Exception as e:
            print(e)
            return JsonResponse({'isError': 'true', 'errorMess': 'server Error.'})

    return HttpResponse("working")


# @api_view(["GET"])
def home(request):
    data = Student.objects.all()
    check = Student.objects.filter(
        department='BCA', year="FY", rollNumber="20bca163")
    print(check)
    context = {}
    data = model_to_dict(check[0])
    # test()
    return Response(data)


# test_webcam()
test_img()
