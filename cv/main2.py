import cv2
import numpy as np
import check_circle
import findcolor
import time
import configparser
# import sendmessage

config = configparser.ConfigParser()
# 读取配置文件
filename = 'config.ini'
config.read(filename, encoding='utf-8')
midX = config.getint('camera', 'x')//2
midY = config.getint('camera','y')//2
state = config.getint('system', 'state')//2

cap = cv2.VideoCapture(0)
cv2.namedWindow('camera2', cv2.WINDOW_AUTOSIZE)

is_cricle=0
i=0
sum=0

while cap.isOpened():
    flag_black = 1
    ret, frame = cap.read()
    if ret:
        if frame is not None:
            flag_black,flag,x,y=findcolor.findcolorCircle(frame,'black','camera2')
            if x==-255:
                flag_black = 0
            driftX=x-midX
            driftY=y-midY
            i+=1
            sum+=flag
            if i==10:
                flag=sum/10
                if flag>=0.2:
                    flag=1
                else:
                    flag=0
                if state == 0:
                    print(flag_black,flag, driftX, driftY)  # 需要发送给control system的消息。格式为是否检测到，偏移量。
                else:
                    try:
                        print(flag_black,flag, driftX, driftY)
                        strs = "CCBB"
                        sendmessage.send(strs,[flag_black,flag, driftX, driftY])
                    except:
                        print("send failed")
                        print(flag_black, flag, driftX, driftY)
                flag=0
                sum=0
                i=0

        else:
            print("无画面")
    else:
        print("无法读取摄像头！")

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()

