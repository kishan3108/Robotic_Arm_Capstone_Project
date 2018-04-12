
#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import time, sleep
from enc_count import enc_count
from PID import PID
from scale import sc1, sc2, sc3
import socket

mot1=19
mot2=26
mot3=13


ctrl1=PID(2.75,1.5,2)
ctrl2=PID(1.75,1,1)
ctrl3=PID(2,0.5,1.2)


GPIO.setwarnings( False )
GPIO.setmode( GPIO.BCM )
GPIO.setup( mot1 , GPIO.OUT )
GPIO.setup( mot2 , GPIO.OUT )
GPIO.setup( mot3 , GPIO.OUT )


m1 = GPIO.PWM( mot1 , 200 )
m2 = GPIO.PWM( mot2 , 200 )
m3 = GPIO.PWM( mot3 , 200 )


m1.start(0)
m2.start(0)
m3.start(0)


m1.ChangeDutyCycle(29)
m2.ChangeDutyCycle(29)
m3.ChangeDutyCycle(29)


pos1=int((raw_input('Please provide count for motor 1: ')) or '0')
if pos1>450000: pos1=450000
pos2=int((raw_input('Please provide count for motor 2: ')) or '0')
if pos2>125000: pos2=125000
pos3=int((raw_input('Please provide count for motor 3: ')) or '0')
if pos3>500000: pos3=500000


ctrl1.SetPoint=pos1
ctrl2.SetPoint=pos2
ctrl3.SetPoint=pos3



while 1:
  a=time()

  enc=enc_count()

  ctrl1.update(enc[0])
  ctrl2.update(enc[1])
  ctrl3.update(enc[2])

  sig1=sc1(ctrl1.output)
  sig2=sc2(ctrl2.output)
  sig3=sc3(ctrl3.output)

  if sig1<=18: sig1=18
  if sig1>=40: sig1=40

  if sig2<=18: sig2=18
  if sig2>=40: sig2=40

  if sig3<=18: sig3=18
  if sig3>=40: sig3=40

  if ctrl1.last_error>4000 and 29<=sig1<=32: sig1=33
  if ctrl1.last_error<-4000 and 26<sig1<=29: sig1=26
  
  if ctrl2.last_error>2000 and 29<=sig2<=32: sig2=33
  if ctrl2.last_error<-2000 and 26<sig2<=29: sig2=26
  
  if ctrl3.last_error>2000 and 29<=sig3<=34: sig3=34  
  if ctrl3.last_error<-2000 and 26<sig3<=29: sig3=26

  m1.ChangeDutyCycle(sig1)     
  m2.ChangeDutyCycle(sig2)
  m3.ChangeDutyCycle(sig3)

  print ctrl1.last_error,"   ",enc[0],"   ",sig1
  print ctrl2.last_error,"   ",enc[1],"   ",sig2
  print ctrl3.last_error,"   ",enc[2],"   ",sig3  
  print "   "
  print "   "
  
  b=time()
  if (b-a)<0.0005: sleep(0.0005-(b-a))
  # To check the loop speed uncomment following 2 lines.
#  c=time()
#  print 1/(c-a)
#  print enc
