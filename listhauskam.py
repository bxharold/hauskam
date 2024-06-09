#!/usr/bin/python3   
 # listhauskam.py 

import sqlite3
from sqlite3 import Error

def index():
  with sqlite3.connect("Hauskam.db") as conn:
    cursor = conn.cursor()
    #cursor.execute("select htime, filename, mailed from hauskam")
    cursor.execute("select * from hauskam")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close() 

if __name__=='__main__':
  index()

