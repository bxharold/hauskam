#!/usr/bin/python3
#  from ~/Git:  tar --exclude=".*" -czvf hauskam_v9.tgz hauskam/ 
#  from ~/Git:  tar --exclude=".*" -cvf hauskam_v9.tgz hauskam/ 

import sqlite3
from sqlite3 import Error
import os, sys, re, time
from datetime import datetime, timedelta
from time import sleep
from picamera import PiCamera
camera = PiCamera()
from gpiozero import MotionSensor, LED
pir = MotionSensor(17)
ledr = LED(26)

sleeptime = 5  # wait before sensing  # 5 test, 5*60 live
emailWaitTime = 20 # 60*60  # wait before sending an email. # 60 min 
email_creds = os.environ["WIN7_HKEY"]  # source ~/smtp.txt
lastMailSentAt = datetime.now() - timedelta(hours=2)
USE_PIR = True  # see  waitForMotion() wrapper

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

s_email = "hfinzz@gmail.com"
from_email_pass = os.environ["WIN7_HKEY"]
s_password = from_email_pass
r_email = ['hfinziot@gmail.com', 'befinz65@gmail.com']
r_email = ['hfinziot@gmail.com']

def send_email(s_email, s_password, r_email, subject, body, att_path):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    port = 587
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = s_email
    msg['To'] = ", ".join(r_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain')) # add body
    # Add file as image/jpeg attachment
    with open(att_path, "rb") as attachment: 
        part = MIMEBase("image", "jpeg")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {att_path}",
    )
    # Add attachment to message and convert message to string
    msg.attach(part)
    text = msg.as_string()
    # Log in to SMTP server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(s_email, s_password)
        server.sendmail(s_email, r_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def drop_create():
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

def insert(conn, tup):
  (created,filename) = tup
  cursor = conn.cursor()
  sql = "INSERT INTO hauskam (created, htime, filename, mailed) VALUES (?,?,?,?) ";
  htime = time.strftime("%m/%d/%Y %I:%M:%S%p")
  mailed = "-"
  newtup = (created, htime, filename, mailed)
  cursor.execute(sql, newtup)
  lastrowid = cursor.lastrowid
  conn.commit()
  cursor.close()
  return lastrowid

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

def list():
  with sqlite3.connect("Hauskam.db") as conn:
    cursor = conn.cursor()
    cursor.execute("select * from hauskam")
    rows = cursor.fetchall()
    for row in rows:
      print(row)
    cursor.close() 

def makeFilename():
  return "static/" + time.strftime("PIC-%m-%d-%I:%M:%S%p.jpg")   

if not USE_PIR:   # --  --  --  --  --  --  --  --  -- 
  # use kbd input to emulate a PIR sensor on a Mac (no GPIO)
  import termios
  def waitForMotion():  # this is the stub for motion_detected
    # ignore enter's that occured during sleep...
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    blockingIO = input("waiting for the enter key")
else:    # --  --  --  --  --  --  --  --  -- 
  def waitForMotion():    # we're using the PIR sensor
    # we're using the PIR sensor
    pir.wait_for_motion()
#  # --  --  --  --  --  --  --  --  --  --  --  --  -- 

def snapSaveSend():
  global lastMailSentAt   # python question: Why global?
  motiondetected = datetime.now()
  ledr.on()
  filename = makeFilename()
  res = (256,192)  # good'nuf, ~ 70kb
  res = (512,384)  # nicer,   ~ 170kb
  snapSave(filename, res)
  with sqlite3.connect("Hauskam.db") as conn:
    lastrowid = insert( conn, (time.time(), filename ) )
    tooSoonToSend = (motiondetected-lastMailSentAt).seconds<emailWaitTime
    if not tooSoonToSend:
      print("send email")   # ... and update log record
      subject = "hauskam notification " + filename
      body = "This email has a JPG attachment.\n\n" + listAsText()
      body = body + "Note, there may be later unsent PICs\n"
      body = body + "Check http://192.168.1.18:5656 for availability\n"
      send_email(s_email, s_password, r_email, subject, body, filename)
      sql = f"UPDATE hauskam SET mailed='SENT' where rowid={lastrowid}"
      conn.execute(sql)
      conn.commit
      lastMailSentAt = datetime.now()
    else:
      print("too soon to send email")
  ledr.off()

def snapSave(filename, res):
    camera.resolution = res  #  (256,192)  is good'nuf
    print(camera.resolution, filename)
    camera.start_preview()
    sleep(2) # Camera warm-up time
    camera.capture(filename)
    camera.stop_preview()
 
def main():
    global lastMailSentAt   # python question: Why global?
    lastMailSentAt = datetime.now() - timedelta(hours=2)  #q&d
    time.sleep(sleeptime)
    for i in range(3):
        waitForMotion()
        snapSaveSend()
        time.sleep(sleeptime)
    list() 

if __name__=='__main__':
  if len(sys.argv) > 1:  # anything will indicate "clear"
    drop_create()  # clears out the database, no change to stored PICs
  main()

"""
To set up environment (not virtual!) that holds the email pwd:    
source ~/smtp.txt

wip backups are named v{n}_hauskam.py and mv'ed to garden: 
HiMac2:~/garden/hauskam mv ~/Git/hauskam/v* .

nice-to-have: 
  querydb.py  flask app that renders all images from the database
  listhauskam.py lists just the database entries

"""
