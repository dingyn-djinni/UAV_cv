# -*- coding: utf-8 -*-
# author:djinni
# 一款仅实现基本的加减乘除括号功能的科学计算器，没怎么测试过，可能有bug
# development enviroment：ubuntu18.04+python3.6+pyqt5

import _thread
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
import sys
from color import Ui_color  # 导入生成form.py里生成的类
from PyQt5 import QtCore
from PyQt5.QtCore import *
import cv2
import numpy as np

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
cv2.namedWindow('picture', cv2.WINDOW_AUTOSIZE)
while cap.isOpened():
    ret, frame = cap.read()
    if frame is not None:
        cv2.imshow('picture', frame)
        cv2.waitKey(1)
    a = input()
    if a=='g':
        break
    else:
        continue
print("ready")

class mywindow(QtWidgets.QWidget, Ui_color):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.sH=0
        self.sS = 58
        self.sV=60
        self.lH=4
        self.lS=255
        self.lV=255
        self.smallHtext.setPlainText(str(self.sH))
        self.smallStext.setPlainText(str(self.sS))
        self.smallVtext.setPlainText(str(self.sV))
        self.largeHtext.setPlainText(str(self.lH))
        self.largeStext.setPlainText(str(self.lS))
        self.largeVtext.setPlainText(str(self.lV))
    def cmpColor(self):
        colorLow=[self.sH,self.sS,self.sV]
        colorHigh=[self.lH,self.lS,self.lV]
        if frame is not None:  # 处理图像的部分
            cv2.imshow('picture', frame)
            cv2.waitKey(1)
            gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯模糊
            hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
            erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细

            inRange_hsv = cv2.inRange(erode_hsv, np.array(colorLow), np.array(colorHigh))
            cv2.imshow('picture_set', inRange_hsv)
            cv2.waitKey(1)
        else:
            print("无画面")
    def capture(self):
        self.cmpColor()
        print(self.sH,self.sS,self.sV)
        print(self.lH,self.lS,self.lV)
    def smallH(self):
        self.sH = self.smallHslider.value()
        self.smallHtext.setPlainText(str(self.sH))
        self.cmpColor()
        return
    def smallV(self):
        self.sV = self.smallVslider.value()
        self.smallVtext.setPlainText(str(self.sV))
        self.cmpColor()
    def smallS(self):
        self.sS = self.smallSslider.value()
        self.smallStext.setPlainText(str(self.sS))
        self.cmpColor()
    def largeV(self):
        self.lV = self.largeVslider.value()
        self.largeVtext.setPlainText(str(self.lV))
        self.cmpColor()
        return
    def lrageS(self):
        self.lS = self.largeSslider_2.value()
        self.largeStext.setPlainText(str(self.lS))
        self.cmpColor()
        return
    def largeH(self):
        self.lH = self.largeHslider.value()
        self.largeHtext.setPlainText(str(self.lH))
        self.cmpColor()
        return

app = QtWidgets.QApplication(sys.argv)
window = mywindow()
window.show()
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
sys.exit(app.exec_())