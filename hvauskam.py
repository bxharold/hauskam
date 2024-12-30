#!/usr/bin/python3
# hvauskam.py, was querydb.py

from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
  with sqlite3.connect("/home/pi/Git/hauskam/Hauskam.db") as conn:
    cursor = conn.cursor()
    cursor.execute("select htime, filename, mailed from hauskam order by htime desc limit 28")
    rows = cursor.fetchall()
    cursor.close() 
    return render_template("index.html", rows=rows)

@app.route('/reset', methods = ['GET','POST'])
def reset():
  with sqlite3.connect("/home/pi/Git/hauskam/Hauskam.db") as conn:
    cursor = conn.cursor()
    cursor.execute("delete  from hauskam;")
    cursor.execute("select htime, filename, mailed from hauskam order by htime desc limit 28")
    rows = cursor.fetchall()
    cursor.close() 
    return render_template("index.html", rows=rows)

if __name__=='__main__':
  a = 5656
  app.run(host="0.0.0.0", port=f"{a}", debug=True)
