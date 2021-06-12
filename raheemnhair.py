import cv2

import numpy as np

from djitellopy import tello

import time

me = tello.Tello()

me.connect()

print(me.get_battery())

me.streamon()

me.takeoff()

me.send_rc_control(0, 0, 31, 0)

time.sleep(2.2)

w, h = 360, 240

kernel = np.ones((5,5),np.float32)/25


#cap = cv2.VideoCapture(1)

def display(img,x=int(w/3),y=2*int(w / 3),u=int(h / 3),v=2*int(h / 3)):
	cv2.putText(img,
				"MA64:obstacle", (30, 10), 2, 1, (255, 255, 255), 2)
	cv2.line(img,
             (x,0),(x,h),
             (255,0,230),
             3)
	cv2.line(img,
            (y, 0), (y, h),
             (255, 0, 230),
             3)
	cv2.line(img,
             (x,u), (y,u),
             (255, 0, 230),
             3)
	cv2.line(img,
             (x,v), (y,v),
             (255, 0, 230),
             3)


while True:

    #_, img = cap.read()
    x = int(w / 3)
    y = 2 * int(w / 3)
    u = int(h / 3)
    v = 2 * int(h / 3)

    img = me.get_frame_read().frame

    img = cv2.resize(img, (w, h))

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    smooth = cv2.filter2D(gray,-1,kernel=kernel)

    #optimal edge detection

    edges = cv2.Canny(smooth,100,200)

    ret3, thres = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    s1 = thres[0:h,0:x]
    s2 = thres[u:v,x:y]
    s3 = thres[0:h,y:w]
    s4 = thres[v:h,x:y]
    s5 = thres[0:u,x:y]

    s1 = np.array(s1)
    s2 = np.array(s2)
    s3 = np.array(s3)
    s4 = np.array(s4)
    s5 = np.array(s5)


    c1 = np.sum(s1 == 255)
    c2 = np.sum(s2 == 255)
    c3 = np.sum(s3 == 255)
    c4 = np.sum(s4 == 255)
    c5 = np.sum(s5 == 255)

    a1 = h * x
    a2 = (v-u) * (y-x)
    a3 = h * (w-y)
    a4 = (y-x) * (h-y)
    a5 = (y-x) * u
    max = 0.3
    min = 0.09

    if c2> 250:
        if c1 < min * a1 and c1 <= c3:
            me.send_rc_control(-17,0,0,0)
            time.sleep(1.3)
            #move left

        elif c3 < min * a3 and c3 <= c1:
            me.send_rc_control(17,0,0,0)
            #move right
            time.sleep(1.3)

        elif c4 < min * a4 and c4 <= c5:

            #move down
            me.send_rc_control(0,0,-17,0)
            time.sleep(1.3)


        elif c1 > max * a1 and c2 > max * a2 and c3 > max * a3 and c4 > max * a4:
            me.send_rc_control(0,0,0,90)
            time.sleep(1.3)
        else:
            #move up
            me.send_rc_control(0,0,17,0)
            time.sleep(1.3)
    else:
        me.send_rc_control(0,20,0,0)
        time.sleep(1.3)
    #print(“Center”, info[0], “Area”, info[1])
    display(thres)
    display(img)
    display(edges)
    display(smooth)
    cv2.imshow("threshold",thres)
    cv2.imshow("canny",edges)
    cv2.imshow("filter",smooth)
    cv2.imshow("Output", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):

        me.land()

        break