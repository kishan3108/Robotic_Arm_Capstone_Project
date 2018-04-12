#!/usr/bin/env python

import mraa
import serial
from PID import PID
from enc_count import enc_count

u=mraa.Uart(0)
u.setBaudRate(115200)

#Lets set the controller in Torque Mode
u.writeStr('^MMOD 1 5_^MMOD 2 5_')

ctrl1=PID(0.5,1.5,0)
ctrl2=PID(0.5,1,0)

a=int((raw_input('please provide count for motor 1: ')) or '0')
if a>450000: a=450000
b=int((raw_input('please provide count for motor 2: ')) or '0')
if b>125000: b=125000

ctrl1.SetPoint=a
ctrl2.SetPoint=b


while 1:
  enc = enc_count()
  ctrl1.update(enc[0])
  ctrl2.update(enc[1])
  sig1=int(ctrl1.output*1000./450000)
  sig2=int(ctrl2.output*1000./175000)
  if -20<=sig1<-4 and ctrl1.last_error<-2000: sig1=-1
  if 4<sig1<=20 and ctrl1.last_error>2000: sig1=1
  if -2000<=ctrl1.last_error<2000 and -3<=sig1<=3: sig1=0
  if -20<=sig2<=4 and ctrl2.last_error<-1000: sig2=-1
  if 4<=sig2<=20 and ctrl2.last_error>1000: sig2=1
  if -1000<=ctrl2.last_error<1000 and -4<sig2<4: sig2=0
  u.writeStr('!G 1 %s_' % sig1)
  u.writeStr('!G 2 %s_' % sig2)
  print ctrl1.last_error,'   ',sig1,'  ',enc[0]
  print ctrl2.last_error,'   ',sig2,'   ',enc[1] 
  print '   '
