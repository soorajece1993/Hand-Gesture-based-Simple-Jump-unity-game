import cv2
import numpy as np
import math
import socket
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cam = cv2.VideoCapture(0)
controlcnt=0
font = cv2.FONT_HERSHEY_SIMPLEX
fontColor = (0, 255, 255)
fontSize = 0.8

while True:
    ret, frame = cam.read()

    if ret:

        cv2.rectangle(frame, (350, 225), (640, 480), (0, 255, 0), 0)
        img = frame
        crop_img = frame[225:480, 350:640]
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        value = (35, 35)

        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # cv2.imshow('Thresholded', thresh1)
        contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, \
                                               cv2.CHAIN_APPROX_NONE)
        max_area = -1

        if contours:
            for i in range(len(contours)):
                cnt = contours[i]
                area = cv2.contourArea(cnt)
                if (area > max_area):
                    max_area = area
                    ci = i
            cnt = contours[ci]
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)
            hull = cv2.convexHull(cnt)
            drawing = np.zeros(crop_img.shape, np.uint8)
            cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
            hull = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull)
            count_defects = 0
            cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
            global xyz
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57
                if angle <= 90:
                    count_defects += 1
                    cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
                # dis
                # t = cv2.pointPolygonTest(cnt,far,True)
                cv2.line(crop_img, start, end, [0, 255, 0], 2)
                # cv2.circle(crop_img,far,5,[0,0,255],-1)


            if count_defects == 3:

                cv2.putText(img, "Hand Open", (50, 50), font, fontSize, fontColor, 2)
                controlcnt=controlcnt+1
                if controlcnt==5:
                    sock.sendto(("JUMP123!").encode(), (UDP_IP, UDP_PORT))

            else:
                cv2.putText(img, "Hand Closed", (50, 50),
                            font, fontSize, fontColor, 2)
                controlcnt=0
            # cv2.imshow('drawing', drawing)
            # cv2.imshow('end', crop_img)
            # cv2.imshow('Gesture', img)


        cv2.imshow('frame', frame)
        key = cv2.waitKey(10)