#!/bin/env python

import os, sys
from upd_database import *

def main():

  LOC = BUILDING, FLOOR = ["", ""]

  conn = sqlite3.connect('pi-fingerprints.db')
  c = conn.cursor()
  path="/home/pi/rssi-raspi/rssi"
  ip = ""
  bssid = ["","",""]
  rssi = [0, 0, 0]

  counter = 0
  fifo = open(path, "r")
  while(True):
    line = fifo.read()
    if (len(line) == 0 or sys.getsizeof(line) > 4):
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
        perceived_loc = get_location(c, bssid[i], rssi[i]).split()
        for l in range(len(perceived_loc)):
          if (len(perceived_loc[l]) != 0):
            LOC[l] = perceived_loc[l]
        BUILDING, FLOOR = LOC
        print(BUILDING + " " + FLOOR)
      counter = 0
      ip = line
      bssid = ["","",""]
      rssi = [0, 0, 0]
    elif (counter % 10 < 4):
      rssi[index] = (rssi[index] << 4) | int(line)
      if (counter == 33):
        print("IP:" + str(ip) + "\tBSSID: " + str(bssid) + "\tRSSI: " + str(rssi))
        for i in range(3):
          perceived_loc = get_location(c, bssid[i], rssi[i]).split()
          for l in range(len(perceived_loc)):
            if (len(perceived_loc[l]) != 0):
              LOC[l] = perceived_loc[l]
          BUILDING, FLOOR = LOC
          print(BUILDING + " " + FLOOR)
        counter = -1
        ip = "" 
        bssid = ["","",""]
        rssi = [0, 0, 0]
    elif (counter % 10 >= 4 and counter % 10 < 9): 
      if (len(bssid[index]) != 0):
        bssid[index] = bssid[index] + ":" + line
      else: 
        bssid[index] = line
    counter = counter + 1
   

main()

