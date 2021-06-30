import cv2
import numpy as np
import findcolor
import configparser
#import sendmessage
config = configparser.ConfigParser()

# 读取配置文件
filename = 'config.ini'
config.read(filename, encoding='utf-8')

midX = config.getint('camera', 'x')//2
midY = config.getint('camera', 'y')//2
state = config.getint('system', 'state')//2

cap = cv2.VideoCapture(1)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)

while cap.isOpened(): # 开启照相机
    ret, frame = cap.read()
    flag_red=1
    flag_green=1
    if ret:
        if frame is not None: #处理图像的部分
            greenX,greenY,greenWidth=findcolor.findcolor(frame,'green','camera')
            redX,redY,redWidth=findcolor.findcolor(frame,'red','camera')
            if greenX==-255 :
                flag_green = 0
            if redX==-255:
                flag_red=0
            driftGreenX=greenX-midX
            driftGreenY=greenY-midY
            driftRedX=redX-midX
            driftRedY=redY-midY
            if abs(driftGreenX)>280:
                flag_green = 0
            if abs(driftRedX)>280:
                flag_red = 0
            if state==0:
                print(flag_green,flag_red,driftGreenX,driftRedX,greenWidth,redWidth)#需要发送给control system的消息。格式为是否检测到，偏移量。
            else:
                try:
                    print(flag_green, flag_red, driftGreenX, driftRedX, greenWidth, redWidth)
                    strs="CCAA"
                    sendmessage.send(strs,[flag_green,flag_red,driftGreenX,driftRedX,greenWidth,redWidth])
                except:
                    print("send failed")
                    print(flag_green, flag_red, driftGreenX, driftRedX, greenWidth, redWidth)
        else:
            print("无画面")
    else:
        print("无法读取摄像头！")

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()