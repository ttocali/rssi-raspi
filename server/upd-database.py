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

def formatquotes(text):
 return '"' + str(text) + '"'

def add_to_db( c, location, bssid, rssi, room):
  c.execute("INSERT INTO " + location + " VALUES ?", (bssid, rssi, room))

def get_prints( c, location ):
  return c.execute("SELECT * FROM" + location)

def get_bssid_prints( c, location, bssid ):
  return c.execute('SELECT * FROM " + location " WHERE BSSID = (?)', (bssid,))

def in_db( c, location, bssid ):
  print(bssid)
  return c.execute('SELECT EXISTS(SELECT * FROM ' + location + ' WHERE BSSID = (?))', (bssid,))

def upd_db( c, location, bssid, rssi, room):
  if ( len(in_db( c, location, bssid )) > 0 ):
    print("BSSID already in DB. Updating values")
    c.execute('UPDATE ' + location + ' SET RSSI = ' + str(rssi) + ', Floor = ' + room + ' WHERE BSSID = ' + bssid)
  else:
    print("BSSID not in DB. Adding entry")
    add_to_db( c, bssid, rssi, room)

def create_table( c, location ):
  location = '"' + location + '"'
  c.execute("CREATE table " + location + " (`BSSID` TEXT UNIQUE, `RSSI` INTEGER, `Floor` TEXT, PRIMARY KEY(BSSID)) WHERE " + location + "NOT EXISTS (SELECT * FROM sqlite_master WHERE type='table'")

def main():
  conn = sqlite3.connect('pi-fingerprints.db')
  c = conn.cursor()
  path="/home/pi/rssi-raspi/rssi"
  ip = ""
  bssid = ["","",""]
  rssi = [0, 0, 0]

  location = raw_input("Where is this(?)").lower()
  location, floor = location.split()
  create_table(c, location)
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
      if (len(ip) != 0):
        ip = ip + "." + line       
      else:
        ip = line
      print("IP: " + ip)
    elif (counter == 34):
      print("IP:" + str(ip) + "\tBSSID: " + str(bssid) + "\tRSSI: " + str(rssi))
      for i in range(3):
        upd_db( c, location, bssid[i], rssi[i], floor)
      counter = 1
      ip = line
      bssid = ["","",""]
      rssi = [0, 0, 0]
    elif (counter % 10 < 4):
      rssi[index] = (rssi[index] << 4) | int(line)
      print("RSSI: " + str(rssi[index]))
      if (counter == 33):
        print("IP:" + str(ip) + "\tBSSID: " + str(bssid) + "\tRSSI: " + str(rssi))
        for i in range(3):
          upd_db( c, location, bssid[i], rssi[i], floor)
        counter = 1
        ip = line
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

