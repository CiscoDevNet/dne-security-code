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
Copyright (c) 2018, Cisco Systems, Inc. All rights reserved.
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
import ciscosparkapi
import json
import os
import requests
from pprint import pprint
# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
import sys
#Mission TODO1: Please add your SPARK_ACCESS_TOKEN and SPARK_ROOM_ID here
SPARK_ACCESS_TOKEN = ""
SPARK_ROOM_ID=""
spark = ciscosparkapi.CiscoSparkAPI(SPARK_ACCESS_TOKEN)

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

#Mission TODO2:  ENTER YOU CLIENT ID AND AMP API KEY HERE
client_id = ""
api_key = ""
#Mission TODO: Enter the standard AMP event id for type of event for Malware... it is 1107296272
event_id = ""
#Mission TODO3: Create the AMP URL
events_url = "https://{}:{}@amp.dcloud.cisco.com/v1/events".format(client_id,api_key)
events1 = getAMP(events_url)
sha_list= {}
#print (json.dumps(events1, indent=4, sort_keys=True))
for events1 in events1["data"]:
    if events1["event_type_id"] == 1107296272:
        sha_list[events1["computer"]["hostname"]] = events1["file"]["identity"]
    else:
        continue

## Mission TODO: Print the List of infected computer hosts and associated SHA values
if sha_list == {}:
    pprint("Mission--- not Complete... !!!!")
else:
    pprint(sha_list)
    message = spark.messages.create(SPARK_ROOM_ID,
    text='MISSION: 0day AMP-SHA-LIST-Creation - I have completed the AMP mission!')
    print(message)
