from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, HttpResponse
from .models import Teacher
from student.models import Student
from json import loads
import base64
from django.core.files import File
from face_recognition import face_encodings, load_image_file, face_locations, face_distance, compare_faces
from modules.handTrackingClass import handDetactor
import cv2
import numpy as np
# Create your views here.

Found_Face = False
img_list = []


def testHandGesture():
    global Found_Face, img_list
    WIDTH, HEIGHT = 1080, 720

    cap = cv2.VideoCapture(0)
    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)

    handDect = handDetactor(maxHands=1, complex=0, detectionCon=0.5)
    gesture_list = []

    allTeacherEncoding = [teacher.get_encodings()
                          for teacher in Teacher.objects.all()]
    i = 0
    while (not Found_Face or i < 5):
        _, img = cap.read()

        if (Found_Face and i < 5):
            i += 1
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_list.append(img)
            continue
        img = handDect.findHands(img, draw=True)
        lmList = handDect.findPosition(img, handNum=0, draw=False)

        if len(lmList) != 0:
            upFing = handDect.upFingers()
            if len(gesture_list) == 20:
                del gesture_list[0]

            gesture_list.append(sum(upFing))
            if (gesture_list[0] == 5 and gesture_list[-1] == 5 and (0 in gesture_list)):
                # print("Found")
                temp_img = handDect.detectFace(img)
                rgb_temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
                faceloc = face_locations(rgb_temp_img)
                if (faceloc):
                    faceEncoding = face_encodings(rgb_temp_img, faceloc)
                    for encoding in faceEncoding:
                        faceDistance = face_distance(
                            allTeacherEncoding, encoding)
                        index = np.argmin(faceDistance)
                        if (faceDistance[index] < 0.5):
                            print(faceDistance[index], "Found")
                            Found_Face = True
                            break
        cv2.imshow("img", img)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break
    cap.release()
    cv2.destroyWindow("img")


# testHandGesture()


def takeAttendance():
    max_c = 0
    index = 0
    face_loc = None
    for i, img in enumerate(img_list):
        face = face_locations(img)
        count = len(face)
        if (count > max_c):
            max_c = count
            index = i
            face_loc = face

    img = img_list[index]

    allStudentEncoding = [std.get_encodings() for std in Student.objects.all()]
    allStudentName = [
        f"{std.name}-{std.rollNumber}" for std in Student.objects.all()]
    imgEncodings = face_encodings(img, face_loc)

    for encoding, faceLocation in zip(imgEncodings, face):
        faceDistance = face_distance(allStudentEncoding, encoding)
        ind = np.argmin(faceDistance)

        cv2.rectangle(img, (faceLocation[3], faceLocation[0]),
                      (faceLocation[1], faceLocation[2]), (255, 0, 0), 2)

        if (faceDistance[ind] < 0.5):
            print(allStudentName[ind], faceDistance[ind])

    cv2.imshow("img", img[:, :, ::-1])
    cv2.waitKey(0)
    print("Attendance Taking...")


if (Found_Face):
    takeAttendance()


def registerTeacher(request, *args, **kwarg):
    data = request.body
    if data:
        try:
            data = loads(data)
            data = data['data']

            with open("temp.jpg", "wb") as file:
                file.write(base64.b64decode(data['img']))

            with open("temp.jpg", 'rb') as file:
                data['img'] = File(file)
                encodings = face_encodings(load_image_file("temp.jpg"))
                encodings = encodings[0].tolist()

                obj = Teacher.objects.create(**data)
                obj.set_encodings(encodings)
                obj.save()
            return JsonResponse({'isError': 'success', 'errorMess': 'New Teacher Register Successfully.'})

        except Exception as e:
            print(e)
            return JsonResponse({'isError': 'true', 'errorMess': 'server Error.'})

    return HttpResponse("working")


def home(request):
    pass
