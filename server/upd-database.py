import sqlite3


def add_to_db( c, bssid, rssi, location ):
  c.execute("INSERT INTO fingerprints VALUES ?", (bssid, rssi, location))

def get_prints( c ):
  return c.execute("SELECT * FROM fingerprints")

def get_bssid_prints( c, bssid ):
  return c.execute("SELECT * FROM fingerprints WHERE id = ?", bssid)

def in_db( c, bssid ):
  return c.execute("SELECT EXISTS(SELECT * FROM fingerprints WHERE id = ?", bssid)

def upd_db( c, bssid, rssi, location ):
  if ( in_db( c, bssid ) ):
    c.execute("UPDATE fingerprints SET RSSI = ?, Location = ? WHERE BSSID = ?", rssi, location, bssid)
  else:
    add_to_db( c, bssid, rssi, location ):


def main():
  conn = sqlite3.connect('pi-fingerpints.db')
  c = conn.cursor()
  while(1):
   

main()

