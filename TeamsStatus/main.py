# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 21:16:20 2023

@author: John
"""

from getTeamsStatus import teamsStatus
from time import sleep
import serial

ser = serial.Serial("COM6", 9600)

while True:
    x = teamsStatus()
    if x:
        ser.write(b'on')
    else:
        ser.write(b'off')
    sleep(5)
    