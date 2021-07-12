import cv2
import numpy as np

import configparser
config = configparser.ConfigParser()
# 读取配置文件
filename = 'config.ini'
config.read(filename, encoding='utf-8')
X_length = config.getint('camera', 'x')
Y_length = config.getint('camera','y')

color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'black': {'Lower': np.array([0, 0, 0]), 'Upper': np.array([10, 10, 10])},
              }

def image_fill(x1,x2,y1,y2,src):
    mask = np.ones([src.shape[0]+2, src.shape[1]+2, 1], np.uint8)   #掩膜
    mask[x1:x2, y1:y2] = 0
    cv2.floodFill(src, mask, (60, 60), (0, 0, 255), cv2.FLOODFILL_MASK_ONLY)
    cv2.imshow('camera', src)
    cv2.waitKey(1)
    return src

def plot_in(plot,cmp1,cmp2):
    for i in range(0,len(plot)):
        if plot[i]<cmp1[i] or plot[i]>cmp2[i]:
            return 0;
    return 1


def image_preprocessing_color(frame,color):
    for i in range(0,X_length):
        for j in range(0,Y_length):
            if plot_in(frame[i],color_dist[color]['Lower'],color_dist[color]['Upper']):
                frame[i]=[0,0,0]
            else:
                frame[i]=[255,255,255]
    return frame
