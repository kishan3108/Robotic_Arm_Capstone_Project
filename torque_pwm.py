#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from enc_count import enc_count
from PID import PID
from scale_torque import sc1, sc2, sc3

mot1=19
mot2=26
mot3=13

ctrl1=PID(3,1.5,0)
ctrl2=PID(0.6,3,0)
ctrl3=PID(4,1,0)

GPIO.setwarnings( False )
GPIO.setmode( GPIO.BCM )

GPIO.setup( mot1 , GPIO.OUT )
GPIO.setup( mot2 , GPIO.OUT )
GPIO.setup( mot3 , GPIO.OUT )

m1 = GPIO.PWM( mot1 , 200 )
m2 = GPIO.PWM( mot2 , 200 )
m3 = GPIO.PWM( mot3 , 200 )


m1.start( 0 )
m2.start( 0 )
m3.start( 0 )

m1.ChangeDutyCycle( 00 )
m2.ChangeDutyCycle( 29 )
m3.ChangeDutyCycle( 29 )

pos1=int((raw_input( 'Please provide count for motor 1: ' )) or '0' )
if pos1>450000: pos1 = 450000
pos2=int((raw_input( 'Please provide count for motor 2: ' )) or '0' )
if pos2>125000: pos2 = 125000
pos3=int((raw_input( 'Please provide count for motor 3: ' )) or '1000' )
if pos3>500000: pos3=500000

ctrl1.SetPoint = pos1
ctrl2.SetPoint = pos2
ctrl3.SetPoint = pos3


while 1:
  enc=enc_count()

  ctrl1.update( enc[0] )
  ctrl2.update( enc[1] )
  ctrl3.update( enc[2] )

  sig1=sc1( ctrl1.output )
  sig2=sc2( ctrl2.output )
  sig3=sc3(ctrl3.output)

  if sig1 <= 24: sig1 = 24
  if sig2 <= 24: sig2 = 24
  if sig3 <= 26: sig3 = 26
  
  if sig1 >= 34: sig1 = 34
  if sig2 > 34: sig2 = 34
  if sig3 >= 32: sig3 = 32

  if ctrl1.last_error>2000 and 29<= sig1<= 30: sig1 = 30
  if ctrl1.last_error<-2000 and 28<=sig1<29: sig1 = 28
  if ctrl2.last_error > 2000 and 29 <= sig2 <= 30: sig2 = 30
  if ctrl2.last_error <- 2000 and 28 <= sig2 < 29: sig2 = 28
  if ctrl3.last_error > 2000 and 29 <= sig3 <= 31: sig3 = 32  
  if ctrl3.last_error < -2000 and 28 < sig3 < 29: sig3 = 28

  m1.ChangeDutyCycle(sig1)     
  m2.ChangeDutyCycle( sig2 )
  m3.ChangeDutyCycle( sig3 )

#  print ctrl1.last_error,"   ",enc[0],"   ",sig1
#  print ctrl2.last_error,"   ",enc[1],"   ",sig2
  print ctrl3.last_error,"   ",enc[2],"   ",sig3  
  print "   "

#  print enc
