# !usr/bin/env python

import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

while 1 :
    ser.readline()


def readCard():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    while 1 :
        line = ser.readline()
        print(line)
        if line:
            return line
