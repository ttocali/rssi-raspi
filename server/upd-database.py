################################################################
# Authors: Christine Hwang (ch458) and Tania Tocalini (tvt9)
# Date:    3-3-2016
# Lab:     Lab 1
# Summary: Commands on the command line control video playback
#          on mplayer
################################################################

#!/bin/env python


import sqlite3
import os

def add_to_db( c, bssid, rssi, location ):
  c.execute("INSERT INTO fingerprints VALUES (?)", (bssid, rssi, location))

def get_prints( c ):
  return c.execute("SELECT * FROM fingerprints")

def get_bssid_prints( c, bssid ):
  return c.execute('SELECT * FROM fingerprints WHERE BSSID = (?)', (bssid,))

def in_db( c, bssid ):
  print(bssid)
  return c.execute('SELECT EXISTS(SELECT * FROM fingerprints WHERE BSSID = (?))', (bssid,))

def upd_db( c, bssid, rssi, location ):
  bssid = "'" + bssid + "'"
  rssi = "'" + str(rssi) + "'"
  location = "'" + location + "'"
  if ( in_db( c, bssid ) ):
    c.execute('UPDATE fingerprints SET RSSI = (?), Location = (?) WHERE BSSID = (?)', (rssi, location, bssid,))
  else:
    add_to_db( c, bssid, rssi, location )

def connect_fifo():
    fifo.close()
    exit()

def main():
  conn = sqlite3.connect('pi-fingerprints.db')
  c = conn.cursor()
  path="/home/pi/rssi-raspi/rssi"
  ip = ["","",""]
  bssid = ["","",""]
  rssi = [0, 0, 0]

  location = raw_input("Where is this(?)")
  counter = 0
  fifo = open(path, "r")
  while(True):
    line = fifo.read()
    if (len(line) == 0):
     continue
    print("read: " + line)
    index = counter / 10 - 1
    print("index: " + str(index))
    if (counter < 4):
      if (len(ip[index]) != 0):
        ip[index] = ip[index] + "." + line       
      else:
        ip[index] = line
      print("IP: " + ip[index])
    elif (counter == 34):
      print("IP:" + str(ip) + "\tBSSID: " + str(bssid) + "\tRSSI: " + str(rssi))
      for i in range(3):
        upd_db( c, bssid[i], rssi[i], location)
      counter = 1
      ip = ["","",line]
      bssid = ["","",""]
      rssi = [0, 0, 0]
    elif (counter % 10 < 4):
      rssi[index] = (rssi[index] << 4) | int(line)
      print("RSSI: " + str(rssi[index]))
      if (counter == 33):
        print("IP:" + str(ip) + "\tBSSID: " + str(bssid) + "\tRSSI: " + str(rssi))
        for i in range(3):
          upd_db( c, bssid[i], rssi[i], location)
        counter = 1
        ip = [line,"",""]
        bssid = ["","",""]
        rssi = [0, 0, 0]
    elif (counter % 10 >= 4 and counter % 10 < 9): 
      if (len(bssid[index]) != 0):
        bssid[index] = bssid[index] + ":" + line
      else: 
        bssid[index] = line
      print("BSSID: " + bssid[index])
    counter = counter + 1
   

main()

