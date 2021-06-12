import cv2

import numpy as np

from djitellopy import tello
from time import sleep
import time
thres = 0.5 # Threshold to detect object

# cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#
# cap.set(3,1280)
# cap.set(4,720)
# cap.set(10,70)
w=1280
h=720
classNames= []
classFile = "coco.names"
with open(classFile,"rt") as f:
	classNames = [line.rstrip() for line in f]#f.read().rstrip("n").split("n")

configPath ="E:/M64/tello/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
#"ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "E:/M64/tello/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


me = tello.Tello()

me.connect()

print(me.get_battery())

me.streamon()

me.takeoff()
#
me.send_rc_control(0, 0, 31, 0)
#
time.sleep(2.2)
#
# w, h = 360, 240
#
# fbRange = [6200, 6800]
#
# pid = [0.4, 0.4, 0]
#
# pError = 0

# def findFace(img):
    #
    # faceCascade = cv2.CascadeClassifier("E:/xml/haarcascade_frontalface_default.xml")
    #
    # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
    #
    # myFaceListC = []
    #
    # myFaceListArea = []
    #
    # for (x, y, w, h) in faces:
    #
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #
    #     cx = x + w // 2
    #

    #     cy = y + h // 2
#         area = w * h
#
#         cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
#
#         myFaceListC.append([cx, cy])
#
#         myFaceListArea.append(area)
#
#     if len(myFaceListArea) != 0:
#
#         i = myFaceListArea.index(max(myFaceListArea))
#
#         return img, [myFaceListC[i], myFaceListArea[i]]
#
#     else:
#
#         return img, [[0, 0], 0]
#
# def trackFace( info, w, pid, pError):
#
#     area = info[1]
#
#     x, y = info[0]
#
#     fb = 0
#
#     error = x - w // 2
#
#     speed = pid[0] * error + pid[1] * (error - pError)
#
#     speed = int(np.clip(speed, -100, 100))
#
#     if area > fbRange[0] and area < fbRange[1]:
#
#         fb = 0
#
#     elif area > fbRange[1]:
#
#         fb = -20
#
#     elif area < fbRange[0] and area != 0:
#
#         fb = 20
#
#     if x == 0:
#
#         speed = 0
#
#         error = 0
#
#     #print(speed, fb)
#
#     me.send_rc_control(0, fb, 0, speed)
#
#     return error

#cap = cv2.VideoCapture(1)
def display(img):
    cv2.putText(img,"MA64:obstacle",
                (30,10),2,1,(255,255,255),2)
    cv2.line(img,
             (int(w/3),0),(int(w/3),h),
             (255,0,230),
             3)
    cv2.line(img,
             (2*int(w / 3), 0), (2*int(w / 3), h),
             (255, 0, 230),
             3)
    cv2.line(img,
             (0,int(h / 3)), (w,int(h / 3)),
             (255, 0, 230),
             3)
    cv2.line(img,
             (0,2*int(h / 3)), (w,2*int(h / 3)),
             (255, 0, 230),
             3)

while True:

    #_, img = cap.read()

    img = me.get_frame_read().frame

    img = cv2.resize(img, (w, h))

    # img, info = findFace(img)
    #
    # pError = trackFace( info, w, pid, pError)

    #print(“Center”, info[0], “Area”, info[1])
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    print(classIds, bbox)

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            if classNames[classId - 1].lower() == "person":
                cx = box[0] + box[2] // 2
                cy = box[1] + box[3] // 2
                area = box[2]*box[3]
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

                if cx <int(w/3):
                    me.send_rc_control(30, 0, 0, 0)
                    sleep(1)
                    me.send_rc_control(0, 30, 0, 0)
                    sleep(1)
                if cx >(2*int(w/3)):
                    me.send_rc_control(-30, 0, 0, 0)
                    sleep(1)
                    me.send_rc_control(0, 30, 0, 0)
                    sleep(1)
                if cy>(2*int(h/3)):
                    me.send_rc_control(0,0,30,0)
                    sleep(1)
                    me.send_rc_control(0,-30,0,0)
                    sleep(1)
                if cx in range((int(w/3)),(2*(int(w/3)))) and cy in range((int(h/3)),(2*(int(h/3)))) :
                    me.send_rc_control(0,0,50,0)
                    sleep(1)




    i = img.copy()
    display(i)
    cv2.imshow("obstacle",i)
    cv2.imshow("Output", img)

    if cv2.waitkey(1) & 0xFF == ord("q"):

        me.land()

        break
# cv2.destroyAllWindows()