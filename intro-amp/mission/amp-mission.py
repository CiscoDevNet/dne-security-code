#!/usr/bin/env python
"""0day Workflow Mission - edit this file
This is your starting point for the 0day workflow  Mission.
Edit this file to
 -
There are a few places to edit (search for MISSION comments)

Script Dependencies:
    requests
Depencency Installation:
    $ pip install requests
Copyright (c) 2019-2020 Cisco and/or its affiliates.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import webexteamssdk
import json
import os
import sys
import requests
from pprint import pprint
from pathlib import Path

# Get the absolute path for the directory where this file is located
here = Path(__file__).parent.absolute()

# Get the path for the project / repository root
project_root = (here/"../../").resolve()

# Extend the system path to include the project root and import the env files
sys.path.insert(0, str(project_root))

import env_lab      # noqa
import env_user     # noqa

# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
from crayons import green

#Intialize the webexteam SDK

teams = webexteamssdk.WebexTeamsAPI(env_user.WEBEX_TEAMS_ACCESS_TOKEN)

# Read the config file evn_user.py to get the AMP API Key settings
client_id = env_user.AMP_CLIENT_ID
api_key = env_user.AMP_API_KEY

print(f""" {green("My AMP Lab Environment:")} 
AMP Host: {env_lab.AMP["host"]} 
 """) 

# Function for the GET Request to the AMP
def getAMP(url):
	try:
	    response = requests.get(url, verify=False)
	    # Consider any status other than 2xx an error
	    if not response.status_code // 100 == 2:
	        return "Error: Unexpected response {}".format(response)
	    try:
	        return response.json()
	    except:
	        return "Error: Non JSON response {}".format(response.text)
	except requests.exceptions.RequestException as e:
	    # A serious problem happened, like an SSLError or InvalidURL
	    return "Error: {}".format(e)


#Enter the standard AMP event id for type of event for Malware... it is 1107296272
event_id = "1107296272"

# Grab the AMP hostname from the lab_evn.py 
host=env_lab.AMP["host"]

#  create the URL for the AMP request 
events_url = "https://{}:{}@{}/v1/events".format(client_id,api_key, host)

events1 = getAMP(events_url)


#Let intialize containers datastructs for different data we will collect from AMP
sha_list= {}
iplist=[]
maclist=[]

#Just in case you want to debug uncomment out the print statement

#print (json.dumps(events1, indent=4, sort_keys=True))
for events1 in events1["data"]:
	if events1["event_type_id"] == 1107296272:
		sha_list[events1["computer"]["hostname"]] = json.dumps(events1["file"]["identity"]) + "\n IP: " + events1["computer"]["network_addresses"][0]["ip"] + "\n Mac: " + events1["computer"]["network_addresses"][0]["mac"]
		iplist.append(events1["file"]["identity"]["sha256"])
		maclist.append(events1["computer"]["network_addresses"][0]["mac"])
	else:
		continue

# In the begining of the file we established the project root directory
wearehere = project_root

# We will write the Mac address list of endpoints where malware executed to a file, 
# ISE Mission script will read this file and nuke these endpoints in quarantine. 
with open(os.path.join(wearehere,"mission-data", "macaddr.txt"), "w") as file:
	file.write(json.dumps(maclist))
file.close()
# We will write the malware SHA list to the file, to be used in ThreatGrid Mission
with open(os.path.join(wearehere, "mission-data", "sha.txt"), "w") as file:
	file.write(json.dumps(iplist))
file.close()

#Finally post the message in the DevNet Express Teams Room and Brag!!!

teams.messages.create(env_user.WEBEX_TEAMS_ROOM_ID, text="AMP Mission completed!!!")
print(green("AMP Mission Completed!!!"))
	