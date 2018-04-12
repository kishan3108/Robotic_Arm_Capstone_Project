#!/usr/bin/env python

# This is the read function which will read the encoder and will provide
# the string of encoder reading.


import serial

ser=serial.Serial('/dev/ttyACM0')

def read():
  sd=ser.readline()
  return sd
