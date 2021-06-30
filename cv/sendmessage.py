# -*- coding:utf-8 -*-
import serial
import time

ser = serial.Serial("/dev/ttyAMA0", 115200)  # 位置1

print('serial test start ...')

def send(strs,data):
    ser.write(strs.encode())  # 位置6
    for i in range(len(data)):
        bytes=floatToBytes(data[i])
        ser.write(bytes)
    time.sleep(0.1)  # 位置8

import struct

def floatToBytes(f):
    bs = struct.pack("f",f)
    bytes = bytes(bs)
    return bytes

if __name__ == '__main__':
    send("hello",[1,2])