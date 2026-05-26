#!/usr/local/bin/python3
#   HiMac2:~/garden/slideshow      hvauskam.py  
#                                  renders  hvauskam.html

import os
from flask import Flask, render_template
import requests
app = Flask(__name__)

hauskam_server = "http://zc.local"

@app.route('/')
def loadpic():
    # Fetch image files from the static directory
    image = "jeanpaulVlizard.jpg"
    ##### get maxid from the ./hpicfilename.py route maxid
    api_url = "http://zc.local:8787/maxid"
    response = requests.get(api_url)
    # Parse the response as JSON (a Python dictionary)
    data = response.json()
    maxid = data["id"]
    return render_template('hvauskam.html', image=image, maxid=maxid)

if __name__ == '__main__':
  a = 8788
  app.run(host="0.0.0.0", port=f"{a}", debug=True)

"""
HiMac2:~/garden/slideshow sqlite3 Hauskam.db  "select *from hauskam where id=8000;"
8000|1778731951.93161|05/13/2026 09:12:31PM|static/PIC-05-13-09:12:31PM.jpg|SENT

hlauskam.py is a good basis for the database part.  Copied here (HiMac2:~/garden/slideshow)
I copied hlauskam.py and the debug version of Hauskam.db here (HiMac2:~/garden/slideshow)

use quareAPI.py as basis for the flask part.. It's really simple.

for the js fetch -- see HiMac2:~/garden/square/spoo-apr-7.txt
Or, garden/sqlare/jchat/daxscript.js 

HiMac2:~/garden/square/eventhandlers   gets too kjpf-specific.

-----------------------------------------
# learner file:  getMaxId.py
#!/usr/local/bin/python3

# Q: I have an API with route /maxid  that returns some json. 
     How do I get those values into my python script?
#    (I've only  been doing the await/fetch API stuff at the JS level)

import requests

# Common Response Methods
# response.json()	When you expect structured JSON data (most common).
# response.text		When you need the raw text string of the response.

api_url = "http://zc.local:8787/maxid"
response = requests.get(api_url)
# Parse the response as JSON (a Python dictionary)
data = response.json()
print(data)
print(data["id"])
-----------------------------------------
"""

