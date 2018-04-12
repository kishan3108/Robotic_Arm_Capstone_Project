#!/usr/bin/env python
import mraa
import serial
from PID import PID
from enc_count import enc_count

u=mraa.Uart(0)
u.setBaudRate(115200)

# Lets set the controller in open loop
u.writeStr('^MMOD 1 0_^MMOD 2 0_')


ctrl1=PID(1.5,3,0)
ctrl2=PID(1,3,0)

a=int((raw_input('please provide count for motor 1: ')) or '0')
if a>450000:
  a=450000
b=int((raw_input('please provide count for motor 2: ')) or '0')
if b>125000:
  b=125000

ctrl1.SetPoint=a
ctrl2.SetPoint=b


while 1:
  enc = enc_count()
  ctrl1.update(enc[0])
  ctrl2.update(enc[1])
  sig1=int(ctrl1.output*1000./425000)
  sig2=int(ctrl2.output*1000./175000)
  if -130<=sig1<=0 and ctrl1.last_error<-1000: sig1=-120
  if 0<=sig1<=130 and ctrl1.last_error>1000: sig1=120
  if -130<=sig2<=0 and ctrl2.last_error<-1000: sig2=-140
  if 0<=sig2<=130 and ctrl2.last_error>1000: sig2=140
  u.writeStr('!G 1 %s_' % sig1)
  u.writeStr('!G 2 %s_' % sig2)
  print ctrl1.last_error,'   ',sig1,'  ',enc[0]
  print ctrl2.last_error,'   ',sig2,'   ',enc[1] 
  print '   '
