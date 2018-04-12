
#!/usr/bin/env python

import RPi.GPIO as GPIO
#from time import time
#from enc_count import enc_count
import socket
from PID import PID
from scale import sc1, sc2, sc3
from read import read
from parse import parse
from sig_check import sig_check
from socket_function import socket_send, socket_receive
from time import gmtime, strftime, time, sleep

mot1=19
mot2=26
mot3=13


ctrl1=PID(2.1,1.15,2)
ctrl2=PID(2.,1,1.5)
ctrl3=PID(1.8,0.5,1.2)

TCP_IP='10.10.10.119'
TCP_PORT=88
BUFFER_SIZE=2048

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#try:
#  s.connect((TCP_IP,TCP_PORT))
#except:
#  pass

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

"""
pos1=int((raw_input('Please provide count for motor 1: ')) or '0')
if pos1>450000: pos1=450000
pos2=int((raw_input('Please provide count for motor 2: ')) or '0')
if pos2>125000: pos2=125000
pos3=int((raw_input('Please provide count for motor 3: ')) or '0')
if pos3>500000: pos3=500000
"""
#pos1=00000
#pos2=00000
#pos3=00000


def gotopoint(a,b,c):
  ctrl1.SetPoint=a
  ctrl2.SetPoint=b
  ctrl3.SetPoint=c



  while 1:
    tm= strftime("%S" , gmtime())
    a=time()
    count=read()
    enc=parse(count)

#  try:
#    s.send(count)
#    s.recv(BUFFER_SIZE)
#  except:
#    pass

#  print enc
  #enc=enc_count()

    ctrl1.update(enc[0])
    ctrl2.update(enc[1])
    ctrl3.update(enc[2])

    sig1=sc1(ctrl1.output)
    sig2=sc2(ctrl2.output)
    sig3=sc3(ctrl3.output)

#  if sig1<=18: sig1=18
#  if sig1>=40: sig1=40

    sig1=sig_check(sig1)
    sig2=sig_check(sig2)
    sig3=sig_check(sig3)

#  if sig2<=18: sig2=18
#  if sig2>=40: sig2=40

#  if sig3<=18: sig3=18
#  if sig3>=40: sig3=40

    if ctrl1.last_error>4000 and 29<=sig1<=32: sig1=33
    if ctrl1.last_error<-4000 and 26<sig1<=29: sig1=26
  
    if ctrl2.last_error>2000 and 29<=sig2<=32: sig2=33
    if ctrl2.last_error<-2000 and 26<sig2<=29: sig2=26
  
    if ctrl3.last_error>2000 and 29<=sig3<=34: sig3=34  
    if ctrl3.last_error<-2000 and 26<sig3<=29: sig3=26

    m1.ChangeDutyCycle(sig1)     
    m2.ChangeDutyCycle(sig2)
    m3.ChangeDutyCycle(sig3)

#  print ctrl1.last_error,"   ",enc[0],"   ",sig1
#  print ctrl2.last_error,"   ",enc[1],"   ",sig2
#  print ctrl3.last_error,"   ",enc[2],"   ",sig3  
#  print "   "
#  print "   "
  #  print tm,' ',enc[0],' ',enc[1],' ',enc[2]
    b=time()
    if (b-a)<0.0005: sleep(0.0005-(b-a))
    c=time()
    print 1/(c-a)
    if -3000<=ctrl1.last_error<=3000 and -2000<=ctrl2.last_error<=2000 and -2000<=ctrl3.last_error<=2000: break

d=[200000,100000,300000,0]
e=[125000,40000,80000,0]
f=[300000,100000,200000,0]

for i in range(len(d)):
  if i<=len(d)-1:
    gotopoint(d[i],e[i],f[i])
#    time.sleep(2)
  else:
    pass
