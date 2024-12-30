#!/usr/bin/python3
#  hmauskam.py  sends email with attached hauskam JPGs
#  sadly this did not work as a cron job. Found alternative.

import sqlite3
from sqlite3 import Error
import os, sys, re, time
from datetime import datetime, timedelta
from time import sleep
from hlauskam import listAsText  # xyz.py is module xyz
appRoot = "/home/pi/Git/hauskam/"

email_creds = os.environ["WIN7_HKEY"]  # source ~/smtp.txt
# This is OK if invoked from CL, but not exec'd by cron-fake.py
# My solution in cron-fake.py is to get the pwd in  ~/smtp.txt,
# then pass it in a f-string in the looping subprocess.run()
# r = subprocess.run(['python3', '/home/pi/Git/hauskam/hmauskam.py'],
#         env=dict(os.environ, WIN7_HKEY=f'{w}'))

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

s_email = "hfinzz@gmail.com"
s_passwd = email_creds 
r_email = ['hfinziot@gmail.com', 'befinz65@gmail.com']
r_email = ['hfinziot@gmail.com']

def send_email(s_email, s_passwd, r_email, subject, body, atts):
    #return
    ## atts is a list of filenames of JPGs 
    # Set up the SMTP server   
    smtp_server = "smtp.gmail.com"
    port = 587
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = s_email
    msg['To'] = ", ".join(r_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain')) # add body

    for att in atts: 
        filename = "/home/pi/Git/hauskam/" + att[0]
        # Add file as image/jpeg attachment
        with open(filename, "rb") as attachment: 
            part = MIMEBase("image", "jpeg")
            part.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        # Add attachment to message and convert message to string
        msg.attach(part)

    text = msg.as_string()
    # Log in to SMTP server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(s_email, s_passwd)
        server.sendmail(s_email, r_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
        print(f"in hmauskam exception handler: pw: {s_passwd}")
    finally:
        print("badness before server.quit() in hmauskam finally")
        server.quit()

def main():
    with sqlite3.connect(appRoot + "Hauskam.db") as conn:
      cursor = conn.cursor() 
      cursor.execute("select filename, id from hauskam where mailed != 'SENT'")
      filenames = cursor.fetchall()
      if len(filenames) > 0:
          x = filenames[0][0][11:]
          subject = "hauskam " + x[:-4]
          body = f"This email has {len(filenames)} JPG attachment(s).\n\n" 
          body = body + "Check http://192.168.1.19:5656 for the most recent 25 pics.\n"
          send_email(s_email, s_passwd, r_email, subject, body, filenames)
          for row in filenames:
              id = row[1]
              sql = f"UPDATE hauskam SET mailed='SENT' where id={id}"
              conn.execute(sql)
              conn.commit
      else:
          x = time.strftime("%m-%d-%I:%M:%S%p")
          subject = f"hauskam {x} -- no new pictures" 
          body = f"This email has no attachment(s).\n\n" 
          body = body + "Check http://192.168.1.19:5656 for the most recent 25 pics.\n"
          send_email(s_email, s_passwd, r_email, subject, body, filenames)
      cursor.close()

if __name__=='__main__':
    #print(listAsText())
    main()
    #print(listAsText())


