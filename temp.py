# from backend.student.models import Student

# Student.objects.all().delete()


import cv2 as cv


def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr


# print(returnCameraIndexes())

cap = cv.VideoCapture(2)

while True:
    _, fram = cap.read()

    cv.imshow("Image", fram)

    if cv.waitKey(1) == ord('q'):
        break
