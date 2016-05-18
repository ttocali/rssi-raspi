#
##############################################################
# Authors: Christine Hwang (ch458) and Tania Tocalini (tvt9)
# Date:    3-3-2016
# Lab:     Lab 1
# Summary: Commands on the command line control video playback
#          on mplayer
################################################################

#!/bin/env python

import sqlite3

def formatquotes(text):
 return '"' + str(text) + '"'

def add_to_db( c, location, bssid, rssi, room):
  c.execute("INSERT INTO " + location + " VALUES (?, ?, ?, ?)", (bssid, rssi, room, 1))

def get_prints( c, location ):
  return c.execute("SELECT * FROM" + location)

def get_bssid_prints( c, location, bssid ):
  return c.execute("SELECT * FROM " + location + " WHERE BSSID = (?)", (bssid,))


def get_frequency(c, location, bssid):
  return c.execute("SELECT NumOfPrint FROM " + location + " WHERE BSSID = (?)", (bssid,)).fetchone()[0]
  

def get_rssi(c, location, bssid):
  return c.execute("SELECT RSSI FROM " + location + " WHERE BSSID = (?)", (bssid,)).fetchone()[0]
  
def get_floor(c, location, bssid):
  return c.execute("SELECT Floor FROM " + location + " WHERE BSSID = (?)", (bssid,)).fetchone()[0]


def in_db_learn( c, location, bssid ):
  test = c.execute("SELECT * FROM " + formatquotes(location) + " WHERE BSSID = (?)", (bssid,))
  return (len(test.fetchall()) > 0)

def in_db_track( c, bssid ):
  tables = c.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'").fetchall()
  for t in tables:
    test = c.execute("SELECT * FROM " + formatquotes(t[0]) + " WHERE BSSID = (?)", (bssid,))
    if ((len(test.fetchall()) > 0)):
      return t[0]
  return ""
  

def upd_db( c, location, bssid, rssi, floor):
  if ( in_db_learn( c, location, bssid )):
    print("BSSID already in DB. Updating values")
    c.execute('UPDATE ' + location + ' SET RSSI = ' 
      + str(get_avgrssi(c, location, bssid, rssi)) + ', Floor = ' 
      + determine_floor(c, location, bssid, rssi, floor) + ", NumOfPrint = " 
      + str(get_frequency(c, location, bssid) + 1) + ' WHERE BSSID = (' + formatquotes(bssid) + ")")
  else:
    print("BSSID not in DB. Adding entry")
    add_to_db( c, location, bssid, rssi, floor)

def create_table( c, location ):
  location = '"' + location + '"'
  if (len(c.execute("SELECT * FROM sqlite_master WHERE type='table' AND tbl_name = " + location).fetchall()) == 0):
    c.execute("CREATE table " + location + " (`BSSID` TEXT UNIQUE, `RSSI` INTEGER, `Floor` TEXT, `NumOfPrint` INTEGER, PRIMARY KEY(BSSID))" )

def get_location(c, bssid, rssi):
  building = in_db_track(c, bssid)
  if (len(building) > 0):
    return building + " " + c.execute("SELECT Floor FROM " + formatquotes(building) + " WHERE BSSID = (?)", (bssid, )).fetchone()[0]
  return building
  
def determine_floor(c, location, bssid, rssi, floor):
  avgrssi = get_rssi(c, location, bssid)
  if (rssi < avgrssi):
    return get_floor(c, location, bssid) 
  return floor
 

def get_avgrssi(c, location, bssid, rssi):
  numrssi = get_frequency(c, location, bssid)
  avgrssi = get_rssi(c, location, bssid)
 
  return (avgrssi + rssi) / 2
