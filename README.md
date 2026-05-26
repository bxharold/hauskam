
# Project hauskam

## PIR motion detection, image capture and email notifications using a raspberry pi zerowh
### Uses gpiozero for the HC-SR501 interface, a sqlite database for event tracking, smtplib for mail notifications, and the python email library for jpg attachments.  Project includes a Flask app to display all PICs recorded in the database.

### v1_hauskam.py was split into h[smrlv]auskam.py by function:  snapper, mailer, rebuilder, utilities, flask viewer.  version 2 abandoned cron, used a cron-fake service instead.

## Components:
- cron-fake.py - workaround to cron's MTA failure, runs as a service
                 execs hmauskam.py hourly. reads gmail creds from ~/smtp.txt, 
                 passes to hmauskam.py as env vbl
- hsauskam.py  - sense/snap/save/wait (loop), runs as a service
- hvauskam.py  - viewer: flask server to display images. Runs as a service on port 8788.
                 requires hpicfilename.py API to be running on port 8787
                 I suppose hpicfilename.py should ALSO be a sevice...
- h5656vauskam.py  - bare-bones viewer: flask server to display images. 
- hpicfilename.py - API.  Runs as a service on port 8788
                 I had to do:  sudo pip install Flask-CORS  (sudo was essential,)
- Hauskam.db   - sqlite3 db. table hauskam stores filenames of snapshots
- hmauskam.py  - mailer -- exec'd by cron-fake.py service
                 To exec from command line, first source ~/smtp.txt
- hrauskam.py  - rebuild Hauskam.db (no effect on images in static/). 
- hlauskam.py  - lister utility functions. 'u' updates all to unsent.
- static/      - All snapshots are stored here
- ~/smtp.txt   - gmail creds. source ~/smtp.txt if exec'd from command line
                 cron-fake reads gmail creds from ~/smtp.txt
- wifipi_info.py    - runs at startup, sends email with IP and service status.
- hhsysctl_stat.sh  - gets IP and service status, is called by wifipi_info.py


##  Usage and Configuration:
### Services (started at bootup)    /lib/systemd/system
- hsauskam.py -- the sense/snap/save/wait loop.
- hvauskam.py -- the flask server for displaying the jpg's
- cron-fake.py -- runs hmauskam.py every hour (replaces a cron task)
     hmauskam.py reads gmail pw from ~/smtp.txt, no env vbl;
       sends recent jpg's as attachments
- wifipi_info.py -- on pi reboot, calls hhsysctl_stat.sh, sends email with IP and service status.

##  Command-line Maintenance::
-   deal wuth static/:  e.g.,  rm -f PIC*
-  ./hrauskam.py a b    # rebuilds the Hauskam.db database
        NOTE: the database is NOT sync'ed with the static/ folder.
        to start with a clean database, first rm Hauskam.db
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
        0. sudo cp X.service  /lib/systemd/system (See text below.)
        1: Reload systemd configuration:
                sudo systemctl daemon-reload
        2: Enable service to start on boot:
                sudo systemctl enable X.service
        3: To add a service to start on boot:
          - add an entry in  /lib/systemd/system
          - sudo systemctl daemon-reload
          - sudo systemctl enable X.service
          - update ~/Git/hauskam/hhsysctl_stat.sh
          - copy that to  ~/hhsysctl_stat.sh
          - refer to the nice documentation Services-systemctl.txt

## Startup:
-  zc is configured to start everything when the Pi is plugged in.

## Shutdown:
1-  Stop the sense/snap/save/wait service 
        sudo systemctl stop hsauskam.service
2-  Stop the cron-fake service 
        sudo systemctl stop cron-fake.service
3-  Run the mailer to clear out the unSENT queue:
        source ~/smtp.txt ; ./hmauskam.py 
4-  sudo shutdown now
== OR IN ONE PASTE: ==
        sudo systemctl stop hsauskam.service
        sudo systemctl stop cron-fake.service
        source ~/smtp.txt ; ./hmauskam.py 
        sudo shutdown now

## BUG:
   - CORS: hpicfilename.py runs from CL, but fails as service.  
     Resolved. ""Since systemd typically runs services as root or 
     a dedicated system user, you need to install the package using 
     sudo so it is accessible globally: "
         sudo pip install -U flask-cors  (sudo was essential.) 

   - absolute paths to the database (resolved.)





## NOTES:
### cron got too complicated vis-a-vis emails, so I wrote cron-fake as a workaround.
```
pi@zc:/lib/systemd/system $ ls -l *ausk* cron-fake*
Jul 16 22:31 cron-fake.service
Dec 22 22:31 hsauskam.service
Jul 16 22:27 hvauskam.service
```
###    cron-fake invokes hmauskam as a subprocess with a (local) env:
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

