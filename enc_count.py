import serial
u=serial.Serial('/dev/ttyACM0')

def enc_count():
  sr=u.readline().replace('/r/n','').split(',')
  try:
    sd=[int(i) for i in sr] #and len(sd)==3
    sd[0] and sd[1] and sd[2]
  except:
    sd= ([0,0,0]) 
  return sd
