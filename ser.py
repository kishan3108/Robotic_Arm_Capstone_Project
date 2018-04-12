import serial

ser=serial.Serial('/dev/ttyACM0')

while 1:
  sr=ser.readline().replace('\r\n','').split(",")
  try:
    sd=[int(i) for i in sr]
    int(sd[0]) and int(sd[1]) and int(sd[2])
    print sd
  except:
    print ([0,0,0])
 
ser.close()
