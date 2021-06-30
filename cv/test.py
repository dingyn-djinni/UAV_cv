import cv2
import numpy as np
import findcolor
import configparser
# import sendmessage
config = configparser.ConfigParser()

# 读取配置文件
filename = 'config.ini'
config.read(filename, encoding='utf-8')

midX = config.getint('camera', 'x')//2
midY = config.getint('camera', 'y')//2
state = config.getint('system', 'state')//2

cap = cv2.VideoCapture(0)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)

while cap.isOpened(): # 开启照相机
    ret, frame = cap.read()
    flag_red=1
    flag_green=1
    if ret:
        if frame is not None: #处理图像的部分
            #findcolor.setColor(frame,'black')
            findcolor.findcolorCircle(frame,'black','camera')
        else:
            print("无画面")
    else:
        print("无法读取摄像头！")

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()