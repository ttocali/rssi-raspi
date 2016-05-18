#!/bin/env python

import os, sys
from db_functions import *

def int32(x):
  if x>0xFFFFFFFF:
    raise OverflowError
  if x>0x7FFFFFFF:
    x=int(0x100000000-x)
    if x<2147483648:
      return -x
    else:
      return -2147483648
  return x

def main():
  conn = sqlite3.connect('pi-fingerprints.db')
  c = conn.cursor()
  path="/home/pi/rssi-raspi/rssi"
  ip = ""
  bssid = ["","",""]
  rssi = [0, 0, 0]

  location = raw_input("Where is this?\n").lower()
  location, floor = location.split()
  create_table(c, location)
  conn.commit()
  counter = 0
  fifo = open(path, "r")
  while(True):
    line = fifo.read()
     
    if (len(line) == 0 or len(line.encode("utf8")) > 4):
     continue
    index = counter / 10 - 1
    if (counter < 4):
      if (len(ip) != 0):
        ip = ip + "." + line       
      else:
        ip = line
    elif (counter == 34):
      print("IP:" + str(ip) + "\tBSSID: " + str(bssid) + "\tRSSI: " + str(rssi))
      for i in range(3):
        upd_db( c, location, bssid[i], rssi[i], floor)
        conn.commit()
      counter = 0
      ip = line
      bssid = ["","",""]
      rssi = [0, 0, 0]
    elif (counter % 10 < 4):
      rssi[index] = (rssi[index] << 8) | int(line)
      rssi[index] = int32(rssi[index])

      if (counter == 33):
        print("IP:" + str(ip) + "\tBSSID: " + str(bssid) + "\tRSSI: " + str(rssi))
        for i in range(3):
          upd_db( c, location, bssid[i], rssi[i], floor)
          conn.commit()
        counter = -1
        ip = "" 
        bssid = ["","",""]
        rssi = [0, 0, 0]
    elif (counter % 10 >= 4 and counter % 10 <= 9): 
      if (len(bssid[index]) != 0):
        bssid[index] = bssid[index] + ":" + line
      else: 
        bssid[index] = line
    counter = counter + 1
   

main()

