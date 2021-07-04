# -*- coding:utf-8 -*-
import serial
import time



# print('serial test start ...')

def send(strs,data):
    ser = serial.Serial("/dev/ttyAMA0", 115200)  # 位置1
    ser.write(strs)  # 位置6
    for i in range(len(data)):
        byte=floatToBytes(data[i])
        ser.write(byte)
    time.sleep(0.1)  # 位置8

import struct

def floatToBytes(f):
    bs = struct.pack("f",f)
    byte = bytes(bs)
    return byte

if __name__ == '__main__':
    print(b'\xcc\xaa')