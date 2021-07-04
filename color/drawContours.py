import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series, DataFrame

def draw():
    img = cv2.imread('lung.png')
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binImg = cv2.threshold(grayImg, 100, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 200, 255), 2)
    plt.imshow(img)
    plt.show()
    print(contours)
    hierarchyDF = DataFrame(hierarchy[0], columns=['pre', 'next', 'child', 'parent'])
    print(hierarchyDF)
draw()