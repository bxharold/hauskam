#!/usr/bin/python3
# picfilename.py   this is the dev version on himac, prod is renamed hpicfilename.py

from flask import Flask, jsonify, request
from flask_cors import CORS     ###  pip3 install Flask-CORS
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

rootdir = "/home/pi/Git/hauskam/"

@app.route("/root/<x>")  # http://127.0.0.1:5000/5
def root(x):
  result = int(x)**0.5
  result = f"{result:.3f}"
  return jsonify({"func": "square root", "result": result})

@app.route("/square/<x>")  # http://127.0.0.1:5000/square/25
def square(x):
  result = int(x)**2
  return jsonify({"func": "square","result": result})

# HiMac2:~/garden/slideshow sqlite3 Hauskam.db  "select *from hauskam where id=8000;"
# 8000|1778731951.93161|05/13/2026 09:12:31PM|static/PIC-05-13-09:12:31PM.jpg|SENT
"""
CREATE TABLE IF NOT EXISTS 'hauskam' (
      id INTEGER PRIMARY KEY,
      created   real,
      htime     varchar(100),
      filename  varchar(200),
      mailed    varchar(10)
      );
"""

@app.route("/maxid")  # return the max id of the pic's in Hauskam.db 
def maxid():
  with sqlite3.connect(rootdir +"Hauskam.db") as conn:
    cursor = conn.cursor()
    cursor.execute(f"select max(id) from hauskam")
    # I may want to add fields, e.g., maxdate, and input date ranges
    row = cursor.fetchone()
    print(row)               #  (8780,)
    if row is None: row = (x,"fileNotFound")
    cursor.close()
  return {"id":row[0], "comma":"curiosity" }      # { "id": 8780 }


@app.route("/pullpic/<int:x>")  # return the pic's filename in Hauskam.db 
def pullpic(x):
  with sqlite3.connect(rootdir +"Hauskam.db") as conn:
    cursor = conn.cursor()
    #cursor.execute(f"select id,filename from hauskam where id={x}")
    #cursor.execute("select id,filename from hauskam where id = ?",  (x,))
    cursor.execute("select id,filename from hauskam where id= :picid", {"picid":x})
    row = cursor.fetchone()
    #print(row)
    if row is None: row = (x,"fileNotFound")
    cursor.close()
  return {"id":row[0], "filename" : row[1] }
  #return jsonify({"id":row[0], "filename" : row[1] })

if __name__ == "__main__":
    port = 8787
    app.run(host="0.0.0.0", port=f"{port}", debug=True)

