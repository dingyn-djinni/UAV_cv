import os
import cv2
import numpy as np
import findcolor

# 判断圆形
def circle(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    #cv2.imshow('camera',gray)
    #cv2.waitKey(1)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=100, param2=30, minRadius=30, maxRadius=0)

    if circles is None:
        return
    circles = circles.astype(int)
    for i in circles[0, :]:
        # print(i)
        cv2.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 2)  # 画圆
        cv2.circle(frame, (i[0], i[1]), 2, (0, 255, 255), 2)  # 画圆心

    # cv2.imwrite('circles.jpg', frame)
    cv2.imshow('camera', frame)
    cv2.waitKey(1)
    return [i[0],i[1]]

def black_circle(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    #cv2.imshow('camera',gray)
    #cv2.waitKey(1)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=100, param2=30, minRadius=30, maxRadius=0)

    if circles is None:
        return
    circles = circles.astype(int)
    for i in circles[0, :]:
        # print(i)
        cv2.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 2)  # 画圆
        cv2.circle(frame, (i[0], i[1]), 2, (0, 255, 255), 2)  # 画圆心

    # cv2.imwrite('circles.jpg', frame)
    cv2.imshow('camera', frame)
    cv2.waitKey(1)
    return [i[0],i[1]]