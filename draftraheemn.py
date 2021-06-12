import cv2
# from djitellopy import tello
import numpy as np
from stack import stackImages
from display_img import display
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,70)
w=1280
h=720

#
import time
#
# me = tello.Tello()
#
# me.connect()
#
# print(me.get_battery())
#
# me.streamon()
#
# me.takeoff()
#
# me.send_rc_control(0, 0, 31, 0)
#
# time.sleep(2.2)
w, h = 360, 240

kernel = np.ones((5, 5), np.float32) / 25


# cap = cv2.VideoCapture(1)




while True:

    # _, img = cap.read()
    _, img = cap.read()

    # img = me.get_frame_read().frame
    x = int(w / 3)
    y = 2 * int(w / 3)
    u = int(h / 3)
    v = 2 * int(h / 3)

    #img = me.get_frame_read().frame

    img = cv2.resize(img, (w, h))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    smooth = cv2.filter2D(gray, -1, kernel=kernel)

    # optimal edge detection

    #edges = cv2.Canny(smooth, 100, 200)
    edges = cv2.Canny(smooth, 30, 100)

    ret3, thres = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    s1 = thres[0:h, 0:x]
    s2 = thres[u:v, x:y]
    s3 = thres[0:h, y:w]
    s4 = thres[v:h, x:y]
    s5 = thres[0:u, x:y]

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
    a2 = (v - u) * (y - x)
    a3 = h * (w - y)
    a4 = (y - x) * (h - y)
    a5 = (y - x) * u
    print((c1,c2,c3,c4,c5))
    max = 0.3
    min = 0.09
    if c2 > 250:                 #max * a2:
        if c1 < 650 and c1 <= c3:
            # me.send_rc_control(-17, 0, 0, 0)
            # time.sleep(1.3)
            # move left
            cv2.putText(img,
                        "left", (int(w/2), int(h/2)), 2, 1, (255, 255, 255), 2)

        elif c3 < 650 and c3 <= c1:
            # me.send_rc_control(17, 0, 0, 0)
            # # move right
            # time.sleep(1.3)
            cv2.putText(img,
                        "right", (int(w/2), int(h/2)), 2, 1, (255, 255, 255), 2)
        elif c4 < 500 and c4 <= c5: # min * a4 and c4 <= c5:
            cv2.putText(img,
                        "down", (int(w/2), int(h/2)), 2, 1, (255, 255, 255), 2)
            # # move down
            # me.send_rc_control(0, 0, -17, 0)
            # time.sleep(1.3)


        elif c1 > 900 and c2 > 400 and c3 > 900 and c4 > 600 and c5 > 600:
            # me.send_rc_control(0, 0, 0, 90)
            # time.sleep(1.3)
            cv2.putText(img,
                        "90 turn", (int(w/2), int(h/2)), 2, 1, (255, 255, 255), 2)
        else:
            # move up
            cv2.putText(img,
                        "UP", (int(w/2), int(h/2)), 2, 1, (255, 255, 255), 2)
    else:
        cv2.putText(img,
                    "continue", (int(w/2), int(h/2)), 2, 1, (255, 255, 255), 2)


            # me.send_rc_control(0, 0, 17, 0)
            # time.sleep(1.3)
    # me.send_rc_control(0, 20, 0, 0)
    # time.sleep(1.3)
    # print(“Center”, info[0], “Area”, info[1])
    display(thres)
    display(img)
    display(edges)
    display(smooth)
    # cv2.imshow("threshold", thres)
    # cv2.imshow("canny", edges)
    # cv2.imshow("filter", smooth)
    # cv2.imshow("Output", img)
    imgStack = stackImages(0.5, ([edges, thres, smooth], [img, img, img]))
    cv2.imshow("ImageStack", imgStack)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        #me.land()

        break
cv2.destroyAllWindows()