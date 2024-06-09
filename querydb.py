#!/usr/bin/python3
# quserydb.py

from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
  with sqlite3.connect("Hauskam.db") as conn:
    cursor = conn.cursor()
    cursor.execute("select htime, filename, mailed from hauskam")
    rows = cursor.fetchall()
    cursor.close() 
    return render_template("index.html", rows=rows)

if __name__=='__main__':
  a = 5656
  app.run(host="0.0.0.0", port=f"{a}", debug=True)
