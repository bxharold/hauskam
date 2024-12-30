#!/usr/bin/python3
#  hsauskam/py   "wait/snap/save"  #  hardware+database.  
#    take pic, record the filename in a Hauskam.db, mark as unsent.
#  Mailing is done by hmauskam, run as a cron-fake.py subprocess. 
#    which sends all unsent pics, marks them as SENT.
 
sleeptime = 0.25*60  # seconds to wait after handling a motion event
cameraWarmUpTime = 0.25*2 # Camera warm-up time
USE_PIR = True  # see  waitForMotion() wrapper
appRoot = "/home/pi/Git/hauskam/"

#  from ~/Git:  tar --exclude=".*" -czvf hauskam_0623.tgz hauskam/ 
#  from ~/Git: tar --exclude="[.|_]*" --exclude='static' -cvf hauskam_0625.tar hauskam/

import sqlite3
from sqlite3 import Error
import os, sys, re, time
from datetime import datetime, timedelta
from time import sleep
from hlauskam import listHauskam
from picamera import PiCamera
from gpiozero import MotionSensor, LED
camera = PiCamera()
pir = MotionSensor(17)
ledr = LED(26)

if not USE_PIR:   # --  --  --  --  --  --  --  --  -- 
  # use kbd input to emulate a PIR sensor on a Mac (no GPIO)
  import termios
  def waitForMotion():  # this is the stub for motion_detected
    # ignore enter's that occured during sleep...
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    blockingIO = input("waiting for the enter key")
else:    # --  --  --  --  --  --  --  --  -- 
  def waitForMotion():    # we're using the PIR sensor
    print("waiting...")
    pir.wait_for_motion()
#  # --  --  --  --  --  --  --  --  --  --  --  --  -- 

def makeFilename():
  # service needs full path; flask server needs relative
  return "static/" + time.strftime("PIC-%m-%d-%I:%M:%S%p.jpg")   

def insertHauskam(conn, created, filename):
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

def snapRecord():
  ledr.on()
  print("snaprecord")
  res = (256,192)  # good'nuf, ~ 70kb
  #res = (512,384)  # nicer,   ~ 170kb
  filename = snapSave(res)
  with sqlite3.connect(appRoot + "Hauskam.db") as conn:
    lastrowid = insertHauskam( conn, time.time(), filename )
  ledr.off()

def snapSave(res):
    camera.resolution = res  
    camera.start_preview()
    sleep(cameraWarmUpTime)  # 2 seconds
    filename = makeFilename()
    camera.capture(appRoot + filename)
    camera.stop_preview()
    print(camera.resolution, filename)
    return filename
 
def main():
    time.sleep(5) # one-time sensor warmup
    for i in range(30000):
        waitForMotion()
        print("got motion", i)
        snapRecord()
        time.sleep(sleeptime)
    listHauskam() 

if __name__=='__main__':
    main()

