
# Project hauskam

## PIR motion detection, image capture and email notifications using a raspberry pi zerowh
### Uses gpiozero for the HC-SR501 interface, a sqlite database for event tracking, smtplib for mail notifications, and the python email library for jpg attachments.  Project includes a Flask app to display all PICs recorded in the database.

### v1_hauskam.py was split into h[smrlv]auskam.py by function:  snapper, mailer, rebuilder, utilities, flask viewer.  version 2 abandoned cron, used a cron-fake service instead.

## Components:
- cron-fake.py - workaround to cron's MTA failure, runs as a service
- hsauskam.py  - snap/save/wait (loop), runs as a service
- hmauskam.py  -  mailer -- exec'd by cron-fake.py service. 
                 The gmail creds are stored in ~/smtp.txt
- hrauskam.py  - rebuild Hauskam.db (no effect on images in static/). 
                 All snapshots are stored in static/
- hlauskam.py  - lister utility functions. 'u' updates all to unsent.
- hvauskam.py  - viewer: flask to display images. Runs as a service.
- Hauskam.db   - sqlite3 db, one table: hauskam


##  Usage and Configuration:
### Services (started at bootup)    /lib/systemd/system
- hsauskam.py -- the snap/save/wait loop.
- hvauskam.py -- the flask server for displaying the jpg's
- cron-fake.py -- runs hmauskam.py every hour (replaces a cron task)
     hmauskam.py reads gmail pw from ~/smtp.txt, no env vbl;
       sends recent jpg's as attachments

##  Command-line Maintenance::
-   ./hrauskam.py a b    # resets the Hauskam.db database
     ( the /reset route is an alt way to reset the Hauskam.db database)
     NOTE: the database is NOT sync'ed with the static/ folder.
-  ./hlauskam.py        # lists hauskam table
-  rm -rf static/*jpg   # removes non-archived jpgs
-  systemctl status cron-fake.service
-  systemctl stop cron-fake.service
-  sudo systemctl status
-  sudo systemctl status X.service
-  sudo systemctl start  X.service
-  sudo systemctl stop   X.service
-  journalctl -u X.service
-  journalctl -r
-  To get X.service to run at boot: (2 steps; I asked gemini.)
  >
        0. sudo cp X.service  /etc/systemd/system (See text below.)
        1: Reload systemd configuration:
                sudo systemctl daemon-reload
        2: Enable service to start on boot:
                sudo systemctl enable X.service

## NOTES:
### cron got too complicated vis-a-vis emails, so I wrote cron-fake as a workaround.
```
pi@zc:/lib/systemd/system $ ls -l *ausk* cron-fake*
Jul 16 22:31 cron-fake.service
Dec 22 22:31 hsauskam.service
Jul 16 22:27 hvauskam.service
```
###    cron-fake invokes hmauskam as a subprocess with a (local?) env:
```
    winky = subprocess.run( ['cat', '/home/pi/smtp.txt'],
            capture_output = True, text = True )
            # ~/smtp.txt : export WIN7_HKEY="xxxx xxxx xxxx xxxx"
    w = winky.stdout.split("\"")[1]
    print(f"__{w}__ __{winky.stdout[7:]}__ __{winky.stderr[7:]}__")
    result = subprocess.run(
          ['python3', '/home/pi/Git/hauskam/hmauskam.py'],
          env=dict(os.environ, WIN7_HKEY=f'{w}'))
```

MORE NOTES: 
-  the database is NOT sync'ed with the static/ folder.
-  cron is no longer used for hauskam. I replaced
```        
# @reboot python3 /home/pi/Git/hauskam/hsauskam.py
```
- with systemctl daemon-reload steps (above.)
