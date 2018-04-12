#!/usr/bin/env python

# This is a parser which will parse the string coming from the 
# teensy and will provide you the list of 3 encoder counts.


def parse(string):
  ps=string.replace('\r\n','').split(",")
  try:
    dt= [int(i) for i in ps]
    if len(dt)==3:
      int(dt[0]) and int(dt[1]) and int(dt[2])
      dt=dt
  except:
    dt=([10,10,10])
  return dt
