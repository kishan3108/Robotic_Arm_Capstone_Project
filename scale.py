#!/usr/bin/env python

def sc1(unscaled): 
  minAllowed=18
  maxAllowed= 40
  min= -450000
  max= 450000
  return int((maxAllowed - minAllowed)*(unscaled - min)/(max - min) + minAllowed)

#print sc1(100000)

def sc2(unscaled):
  minAllowed=17
  maxAllowed= 41
  min= -125000
  max= 125000
  return int((maxAllowed - minAllowed)*(unscaled - min)/(max - min) + minAllowed)

#print sc2(100000)

def sc3(unscaled):
  minAllowed=18
  maxAllowed= 40
  min= -500000
  max= 500000
  return int((maxAllowed - minAllowed)*(unscaled - min)/(max - min) + minAllowed)

