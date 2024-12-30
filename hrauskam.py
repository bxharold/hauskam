#!/usr/bin/python3
#  hruaskam.py  just the database drop/create stuff.
#  ... and for some reason?, the list* functions.

import sqlite3
from sqlite3 import Error
import sys
from datetime import datetime, timedelta

def drop_create(): # rebuild database, no change to stored PICs
  with sqlite3.connect("Hauskam.db") as conn:
    cursor = conn.cursor()
    sql = "DROP TABLE IF EXISTS 'hauskam';"
    cursor.execute(sql)
    sql = """
      CREATE TABLE IF NOT EXISTS 'hauskam' (
      id INTEGER PRIMARY KEY,
      created   real,
      htime     varchar(100),
      filename  varchar(200),
      mailed    varchar(10)
      );
      """
  cursor.execute(sql)
  conn.commit()
  cursor.close() 

def main():
    drop_create()  # no change to stored PICs

if __name__=='__main__':
    if len(sys.argv) < 3:
        print("use 2 clp's to rebuild the database.")
    else:
        main()

