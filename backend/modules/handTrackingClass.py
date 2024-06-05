import mediapipe as mp
import cv2
from time import time
import face_recognition


class handDetactor():
    def __init__(self, imgMode=False, maxHands=2, complex=1, detectionCon=0.5, trackingCon=0.5):
        self.imgMode = imgMode
        self.maxHands = maxHands
        self.complex = complex
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.imgMode, self.maxHands, self.complex, self.detectionCon, self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipId = [4, 8, 12, 16, 20]
        self.hleft = False
        self.hright = False

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if (self.result.multi_hand_landmarks):
            for handLm in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLm, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNum=0, draw=True):
        self.lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNum]

            for id, lm in enumerate(myHand.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x*w), int(lm.y * h)
                self.lmList.append([id, cx, cy])

                if draw:
                    cv2.putText(img, str(id), (cx, cy),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        return self.lmList

    def upFingers(self):
        upFingersList = []

        for hand in self.result.multi_handedness:
            handType = hand.classification[0].label
            if (handType == 'Left'):
                self.hright = True
                if (self.lmList[self.tipId[0]][1] > self.lmList[self.tipId[0]-1][1]):
                    upFingersList.append(1)
                else:
                    upFingersList.append(0)
            else:
                self.hright = False

            if (handType == 'Right'):
                self.hleft = True
                if (self.lmList[self.tipId[0]][1] < self.lmList[self.tipId[0]-1][1]):
                    upFingersList.append(1)
                else:
                    upFingersList.append(0)
            else:
                self.hleft = False

        for tip in range(1, 5):
            if (self.lmList[self.tipId[tip]][2] < self.lmList[self.tipId[tip]-2][2]):
                upFingersList.append(1)
            else:
                upFingersList.append(0)

        return upFingersList

    def detectFace(self, img):
        if (self.hright):
            sy = self.lmList[12][2]-200
            sx = self.lmList[4][1]-200

            ex = sx+600
            ey = sy+600

        if (self.hleft):
            ey = self.lmList[12][2]+400
            ex = self.lmList[4][1]+300

            sx = ex-800
            sy = ey-800
        rh, rw, _ = img.shape
        sx = 0 if sx < 0 else sx
        sy = 0 if sy < 0 else sy
        ex = rw if ex > rw else ex
        ey = rh if ey > rh else ey

        # cv2.rectangle(img, (sx, sy), (ex, ey), (255, 0, 0), 2)
        return img[sy:ey, sx:ex]


def main():

    WIDTH, HEIGHT = 1080, 720

    cap = cv2.VideoCapture(1)
    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)

    pretime = 0
    currtime = 0
    handDect = handDetactor(maxHands=1, complex=0, detectionCon=0.7)
    gesture_list = []
    while True:
        _, img = cap.read()
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
                faceloc = face_recognition.face_locations(rgb_temp_img)
                if (faceloc):
                    print(faceloc)

            # print(upFing, gesture_list)

        # if(len(lmList) != 0):
        #     print(lmList[4])

        currtime = time()
        fps = 1//(currtime-pretime)
        pretime = currtime
        cv2.putText(img, str(fps), (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)

        cv2.imshow("img", img)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break


if __name__ == '__main__':
    main()
