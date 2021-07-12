# -*- coding: utf-8 -*-
# author:djinni
# 一款仅实现基本的加减乘除括号功能的科学计算器，没怎么测试过，可能有bug
# development enviroment：ubuntu18.04+python3.6+pyqt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
import sys
from canvas import Ui_dialog  # 导入生成form.py里生成的类
from PyQt5 import QtCore
from PyQt5.QtCore import *
import cv2
import numpy as np
from threading import Thread
import sys, os, time
import inspect
import ctypes
import imgProcessing
import configparser
import sendmessage

# 预设分辨率参数
config = configparser.ConfigParser()
# 读取配置文件
filename = 'config.ini'
config.read(filename, encoding='utf-8')

midX = config.getint('camera', 'x')//2
midY = config.getint('camera', 'y')//2

# 线程相关函数
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
# 关闭线程
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class mywindow(QtWidgets.QWidget, Ui_dialog):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        cv2.namedWindow('picture', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('picture2', cv2.WINDOW_AUTOSIZE)
        self.lowRedH.setValue(0)
        self.lowRedS.setValue(53)
        self.lowRedV.setValue(68)
        self.highRedH.setValue(5)
        self.highRedS.setValue(255)
        self.highRedV.setValue(255)
        self.lowGreenH.setValue(59)
        self.lowGreenS.setValue(58)
        self.lowGreenV.setValue(33)
        self.highGreenH.setValue(92)
        self.highGreenS.setValue(248)
        self.highGreenV.setValue(113)
        self.lowBlackH.setValue(0)
        self.lowBlackS.setValue(0)
        self.lowBlackV.setValue(0)
        self.highBlackH.setValue(255)
        self.highBlackS.setValue(255)
        self.highBlackV.setValue(100)

    # 测试图像线程
    def getImg1(self,picture):
        cap = cv2.VideoCapture(self.testCamID.value())
        print(self.testCamID.value())
        while cap.isOpened() :
            ret, self.frame = cap.read()
            if self.frame is not None:
                if self.debugMode.isChecked()==True:
                    cv2.imshow(picture, self.frame)
                    cv2.waitKey(1)
    # 前置摄像头线程
    def frontImg(self,picture):
        cap = cv2.VideoCapture(self.frontCameraID.value())
        flag_red = 1
        flag_green = 1
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                if frame is not None:
                    greenX, greenY, greenWidth = imgProcessing.findcolor(frame, [self.lowGreenH.value(),
                                                                                 self.lowGreenS.value(),
                                                                                 self.lowGreenV.value()],
                                                                         [self.highGreenH.value(),
                                                                          self.highGreenS.value(),
                                                                          self.highGreenV.value()], 'picture', 'green',
                                                                         self.debugMode.isChecked())
                    redX, redY, redWidth = imgProcessing.findcolor(frame, [self.lowRedH.value(), self.lowRedS.value(),
                                                                           self.lowRedV.value()],
                                                                   [self.highRedH.value(), self.highRedS.value(),
                                                                    self.highRedV.value()], 'picture', 'red',
                                                                   self.debugMode.isChecked())
                    if greenX == -255:
                        flag_green = 0
                    if redX == -255:
                        flag_red = 0
                    driftGreenX = greenX - midX
                    driftGreenY = greenY - midY
                    driftRedX = redX - midX
                    driftRedY = redY - midY
                    if abs(driftGreenX) > 280:
                        flag_green = 0
                    if abs(driftRedX) > 280:
                        flag_red = 0
                    if self.transferMode.isChecked() == False:
                        print(flag_green, flag_red, driftGreenX, driftRedX, greenWidth,
                              redWidth)  # 需要发送给control system的消息。格式为是否检测到，偏移量。
                    else:
                        try:
                            print(flag_green, flag_red, driftGreenX, driftRedX, greenWidth, redWidth)
                            strs = b'\xcc\xaa'
                            sums = sum([flag_green, flag_red, driftGreenX, driftRedX, greenWidth, redWidth])
                            sendmessage.send(strs,
                                             [flag_green, flag_red, driftGreenX, driftRedX, greenWidth, redWidth, sums])
                        except:
                            print("send failed")
                            print(flag_green, flag_red, driftGreenX, driftRedX, greenWidth, redWidth)
                    if self.debugMode.isChecked() == True:
                        cv2.imshow(picture, frame)
                        cv2.waitKey(1)
                else:
                    print("无画面")
            else:
                print("无法读取摄像头！")


    # 底部摄像头线程
    def bottomImg(self,picture):
        cap = cv2.VideoCapture(self.bottomCameraID.value())
        is_cricle = 0
        i = 0
        sum = 0
        while cap.isOpened():
            flag_black = 1
            ret, frame = cap.read()
            if ret:
                if frame is not None:
                    flag_black, flag, x, y = imgProcessing.findcolorCircle(frame,[self.lowBlackH.value(), self.lowBlackS.value(), self.lowBlackV.value()],[self.highBlackH.value(), self.highBlackS.value(), self.highBlackV.value()],'picture2','black',self.debugMode.isChecked(),self.grayMode.isChecked())
                    if x == -255:
                        flag_black = 0
                    driftX = x - midX
                    driftY = y - midY
                    i += 1
                    sum += flag
                    if i == 10:
                        flag = sum / 10
                        if flag >= 0.2:
                            flag = 1
                        else:
                            flag = 0
                        if self.transferMode.isChecked() == False:
                            print(flag_black, flag, driftX, driftY)  # 需要发送给control system的消息。格式为是否检测到，偏移量。
                        else:
                            try:
                                print(flag_black, flag, driftX, driftY)
                                strs = b'\xcc\xbb'
                                sendmessage.send(strs, [flag_black, flag, driftX, driftY])
                            except:
                                print("send failed")
                                print(flag_black, flag, driftX, driftY)
                        flag = 0
                        sum = 0
                        i = 0
                else:
                    print("无画面")
            else:
                print("无法读取摄像头！")

    # 开启摄像按键
    def pressCutButton(self):
        self.thread_01 = Thread(target=self.getImg1,args=('picture',))
        self.thread_01.start()
        return

    # 阈值对比函数
    def pressCmpButton(self):
        print("cmp_button")
        if self.redRadio.isChecked()==True:
            self.sH, self.sS, self.sV=self.lowRedH.value(),self.lowRedS.value(),self.lowRedV.value()
            self.lH, self.lS, self.lV=self.highRedH.value(),self.highRedS.value(),self.highRedV.value()
        elif self.greenRadio.isChecked()==True:
            self.sH, self.sS, self.sV = self.lowGreenH.value(), self.lowGreenS.value(), self.lowGreenV.value()
            self.lH, self.lS, self.lV = self.highGreenH.value(), self.highGreenS.value(), self.highGreenV.value()
        elif self.blackRadio.isChecked()==True:
            self.sH, self.sS, self.sV = self.lowBlackH.value(), self.lowBlackS.value(), self.lowBlackV.value()
            self.lH, self.lS, self.lV = self.highBlackH.value(), self.highBlackS.value(), self.highBlackV.value()
        else:
            return
        colorLow = [self.sH, self.sS, self.sV]
        colorHigh = [self.lH, self.lS, self.lV]
        if self.frame is not None:  # 处理图像的部分
            gs_frame = cv2.GaussianBlur(self.frame, (5, 5), 0)  # 高斯模糊
            hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
            erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
            inRange_hsv = cv2.inRange(erode_hsv, np.array(colorLow), np.array(colorHigh))
            cv2.imshow('picture2', inRange_hsv)
            cv2.waitKey(1)
        else:
            print("无画面")
        return

    # 前置摄像头
    def pressCam1(self):
        try:
            stop_thread(self.thread_01)
        except:
            print("no thread1")
        self.thread_02 = Thread(target=self.frontImg, args=('picture',))
        self.thread_02.start()
        return

    # 底部摄像头
    def pressCam2(self):
        try:
            stop_thread(self.thread_01)
        except:
            print("no thread1")
        self.thread_03 = Thread(target=self.bottomImg, args=('picture2',))
        self.thread_03.start()
        return

    # 关闭程序
    def pressShut(self):
        try:
            stop_thread(self.thread_01)
        except:
            print("no thread1")
        try:
            stop_thread(self.thread_02)
        except:
            print("no thread2")
        try:
            stop_thread(self.thread_03)
        except:
            print("no thread3")
        exit(0)
        return

    # 输出参数
    def pressLog(self):
        print("red",self.lowRedH.value(),self.lowRedS.value(),self.lowRedV.value())
        print("red",self.highRedH.value(),self.highRedS.value(),self.highRedV.value())
        print("green",self.lowGreenH.value(), self.lowGreenS.value(), self.lowGreenV.value())
        print("green", self.highGreenH.value(), self.highGreenS.value(), self.highGreenV.value())
        print("black",self.lowBlackH.value(), self.lowBlackS.value(), self.lowBlackV.value())
        print("black",self.highBlackH.value(), self.highBlackS.value(), self.highBlackV.value())
        return


    # 截取屏幕按键
    def pressGetImage(self):
        try:
            stop_thread(self.thread_01)
        except:
            print("no thread1")
            return
        print("img get!")
        cv2.imshow('picture', self.frame)
        cv2.waitKey(1)
        return

    def shutCam1(self):
        try:
            stop_thread(self.thread_02)
        except:
            print("no thread2")

    def shutCam2(self):
        try:
            stop_thread(self.thread_03)
        except:
            print("no thread3")


app = QtWidgets.QApplication(sys.argv)
window = mywindow()
window.setWindowTitle("UAV Canvas")
window.show()
sys.exit(app.exec_())
