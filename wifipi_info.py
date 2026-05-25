#!/usr/bin/python3
# wifipi_info.py    google app name hfwifi    5/20/2026  Only for RPi
#                   calls hhsysctl_stat.sh 
import datetime
from time import sleep
import os, sys, subprocess
import smtplib
from email.mime.text import MIMEText

homepath = "/home/pi/"
# get email_creds
winky = subprocess.run( ['cat', homepath+'smtp.txt'],
        capture_output = True, text = True )
email_creds = winky.stdout.split("\"")[1]
#print(f"_{email_creds}_ _{winky.stdout[7:]}_ _{winky.stderr[7:]}_")

s_email = "hfinzz@gmail.com"
s_passwd = email_creds 
r_email = ['hfinzphd@gmail.com','hfinziot@gmail.com']

def wifi_info():
  isPi = os.popen(homepath + "hhsysctl_stat.sh").readlines()
  # pi@zc:~ $ ./hhsysctl_stat.sh
  # zc
  # 192.168.1.19
  # "Raspbian GNU/Linux 11 (bullseye)"
  # hsauskam.service is : disabled
  # hvauskam.service is : enabled
  # cron-fake.service is : disabled
  return isPi

def SendTextMail(hostname, ip, body, readyToSend="NO"):
    timestamp = datetime.datetime.now().strftime("%A %b %d %H:%M%p")
    text = f"{ip}  {hostname}  was rebooted on {timestamp}\n\n{body}" 
    msg = MIMEText(text)
    #print(f"\n\n\n{msg}\n\n\n")
    msg['Subject'] = f"{hostname} {ip} reboot {timestamp}"
    msg['From'] = s_email
    msg['To'] =   ", ".join(r_email)
    if readyToSend == "YES":
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(s_email, email_creds)
        s.sendmail(s_email, r_email, msg.as_string())
    else:
        print(f"\n\n=====TESTING=====\n{msg.as_string()}=====")

readyToSend="YES"    # set this to YES when done testing
if readyToSend=="YES": sleep(2)
isPi = wifi_info()  # a list of strings
body = "".join(isPi)
SendTextMail( isPi[0].strip(), isPi[1].strip(), body, readyToSend )

