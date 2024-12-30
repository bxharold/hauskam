#!/usr/bin/python3
#                                       cron-fake.py
#  cron-fake.py is a simple looper (a seperate process) that
#  I use as a substitute for a cron job that executes hourly.
#  I couldn't get cron to execute hmauskam.py
#    (pi) CMD (python3 /home/pi/Git/hauskam/hmauskam.py)
#    (CRON) info (No MTA installed, discarding output)
#  []Odd. ~/wifipi_info.py cron'ed fine, MIME text vs multipart?
#  I do not want to set up a postfix mail server. (Overkill?)
#  I do not embed the passwd in my code. I set the pwd as an
#  an env vbl, by sourcing ~/smtp.txt. I couldn't figure out how
#  to get subprocess.run() to use the env vbl, so I did this:
#  Since smtp.txt is one line...
#      e.g.,   export WIN7_HKEY="blah blah blah blah"
#  ... I read the file, parse out the pw, f-string it into 
#  the env dict as SOF suggested:
#  https://stackoverflow.com/questions/41171791/
#    how-to-suppress-or-capture-the-output-of-subprocess-run

timeBetweenEmails = 60*60     # one hour
numerOfIterations = 2*24*7    # one email per hour for 2 weeks 
# for sensible testing:
#timeBetweenEmails = 2*60  # 6 minutes
#numerOfIterations = 100        # expecting it'll be ctrl-C'ed

import sys
import os
import time
import subprocess

winky = subprocess.run( ['cat', '/home/pi/smtp.txt'],
        capture_output = True, text = True )
w = winky.stdout.split("\"")[1]
print(f"__{w}__ __{winky.stdout[7:]}__ __{winky.stderr[7:]}__")

for i in range(numerOfIterations):
  result = subprocess.run(
         ['python3', '/home/pi/Git/hauskam/hmauskam.py'],
         env=dict(os.environ, WIN7_HKEY=f'{w}'))
  time.sleep(timeBetweenEmails)
  print(f'{i} {time.strftime("%m-%d-%I:%M:%S%p")}')

