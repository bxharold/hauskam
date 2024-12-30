#!/usr/bin/python3   
#   hlauskam.py   was listhauskam.py 

import sqlite3
from sqlite3 import Error
import sys

def listHauskam():  #  "list()" isn't a smart name
  with sqlite3.connect("Hauskam.db") as conn:
    cursor = conn.cursor()
    cursor.execute("select * from hauskam")
    rows = cursor.fetchall()
    for row in rows:
      print(row)
    cursor.close()

def listAsText():
  with sqlite3.connect("Hauskam.db") as conn:
    cursor = conn.cursor()
    cursor.execute("select id, htime, filename, mailed, created from hauskam")
    rows = cursor.fetchall()
    y = ""
    for row in rows:
       y = y + f"{row[0]}  {row[1]}  {row[2]}  {row[3]} \n"
    cursor.close()
    return y

def markAsUnsent():
    with sqlite3.connect("Hauskam.db") as conn: 
        sql = f"UPDATE hauskam SET mailed='-'"
        conn.execute(sql)
        conn.commit

if __name__=='__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "u":
            markAsUnsent()
    listHauskam()

