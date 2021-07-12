import cv2
import numpy as np

# 找到目标色块
def findcolor(frame,colorLow,colorHigh,camera,ball_color,debugMode):
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
    inRange_hsv = cv2.inRange(erode_hsv, np.array(colorLow), np.array(colorHigh))
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    if len(cnts) == 0:
        return -255,-255,0
    c = max(cnts, key=cv2.contourArea)
    if len(c)<=90:
        return -255, -255,0
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    if ball_color=='red':
        cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
    if ball_color=='green':
        cv2.drawContours(frame, [np.int0(box)], -1, (0, 0, 0), 2)
    if ball_color=='black':
        cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
    centerpointX = int(sum(box[:, 0]) // 4)
    centerpointY = int(sum(box[:, 1]) // 4)
    centerpoint = (centerpointX, centerpointY)
    width=abs(box[0,0]-box[1,0])
    if debugMode==True:
        cv2.imshow(camera, frame)
        cv2.waitKey(1)
    return centerpointX,centerpointY,int(width)

def findcolorCircle(frame,colorLow,colorHigh,camera,ball_color,debugMode,grayMode):
    flagBlack=0
    flagCircle=0
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
    inRange_hsv = cv2.inRange(erode_hsv, np.array(colorLow), np.array(colorHigh))
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    if len(cnts) == 0:
        return 0,0,-255,-255
    c = max(cnts, key=cv2.contourArea)
    if len(c)<=50:
        return 0,0,-255,-255
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    centerpointX = int(sum(box[:, 0]) // 4)
    centerpointY = int(sum(box[:, 1]) // 4)
    if ball_color=='black':
        cv2.drawContours(frame, c, -1, (255, 0, 0),2)
        cv2.fillPoly(frame, [c], (255, 0, 0))
        new_hsv = cv2.inRange(frame, np.array([255,0,0]), np.array([255,0,0]))
        flagBlack=1
        # 进行中值滤波
        img = cv2.medianBlur(new_hsv, 5)
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=20, minRadius=30, maxRadius=600)
        if circles is not None:
            print("get")
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 2)  # 画圆
                cv2.circle(img, (i[0], i[1]), 2, (255, 0, 0), 2)  # 画圆心
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 0, 255), 2)  # 画圆
                cv2.circle(frame, (i[0], i[1]), 2, (255, 0, 0), 2)  # 画圆心
            flagCircle = 1
    if debugMode==True and grayMode==True:
        cv2.imshow(camera, img)
        cv2.waitKey(1)
    if debugMode==True and grayMode==False:
        cv2.imshow(camera, frame)
        cv2.waitKey(1)
    return flagBlack,flagCircle,centerpointX,centerpointY