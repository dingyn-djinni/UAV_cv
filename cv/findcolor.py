import cv2
import numpy as np


color_dist = {'red': {'Lower': np.array([0, 53, 68]), 'Upper': np.array([5, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([59,58,33]), 'Upper': np.array([92,248,113])},
              'black': {'Lower': np.array([0, 0, 0]), 'Upper': np.array([255,255,100])},
              }

# 找到目标色块
def findcolor(frame,ball_color,camera):
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
    inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    if len(cnts) == 0:
        cv2.imshow(camera, frame)
        cv2.waitKey(1)
        return -255,-255,0
    c = max(cnts, key=cv2.contourArea)
    if len(c)<=90:
        cv2.imshow(camera, frame)
        cv2.waitKey(1)
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
    cv2.imshow(camera, frame)
    cv2.waitKey(1)
    return centerpointX,centerpointY,int(width)

def findcircle(frame,ball_color,camera):
    flag=0
    font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
    kernel = np.ones((5, 5), np.uint8)  # 卷积核
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 转换为HSV空间
    #  消除噪声
    mask = cv2.inRange(hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])  # 设定掩膜取值范围
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 形态学开运算
    bila = cv2.bilateralFilter(mask, 10, 200, 200)  # 双边滤波消除噪声
    edges = cv2.Canny(bila, 50, 100)  # 边缘识别
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    c = max(cnts, key=cv2.contourArea)
    # 识别圆形
    circles = cv2.HoughCircles(
        mask, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=70, minRadius=30, maxRadius=500)
    if circles is not None:  # 如果识别出圆
        for circle in circles[0]:
            #  获取圆的坐标与半径
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])
            cv2.circle(frame, (x, y), r, (0, 0, 255), 3)  # 标记圆
            cv2.circle(frame, (x, y), 3, (255, 255, 0), -1)  # 标记圆心
            text = 'x:  ' + str(x) + ' y:  ' + str(y)
            flag=1
            return flag
    cv2.imshow(camera, frame)
    cv2.waitKey(1)
    return flag

def setColor(frame,ball_color):
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细

    inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
    cv2.imshow('camera2', inRange_hsv)
    cv2.waitKey(1)
    cv2.imshow('camera', frame)
    cv2.waitKey(1)

def findcolorCircle(frame,ball_color,camera):
    flagBlack=0
    flagCircle=0
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
    inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
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
            flagCircle = 1
    cv2.imshow(camera, img)
    cv2.waitKey(5)
    return flagBlack,flagCircle,centerpointX,centerpointY