#!/usr/bin/env python

# This is a sig_check for min and max signal values 
# this will keep signal between 18 and 40.

def sig_check(sig):
  if sig<=18: s=18
  elif sig>=40: s=40
  else: s=sig
  return s

