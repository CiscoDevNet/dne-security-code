#!/usr/bin/env python
"""AMP-CODE - edit this file
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
import requests
import json

# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


#function definitions
def get(url):
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

#main code TODO: ENTER YOU CLIENT ID AND API KEY HERE
client_id = "1512e5b0c0c2f2b85401"
api_key = "eaef340f-0ccd-46a5-bcd3-dd62dcbdfb02"

#TODO: Enter the specific event you are interested in to find from the result for example malware execute event id is 1107296272
event_id=1107296272

events_url = "https://{}:{}@amp.dcloud.cisco.com/v1/events".format(client_id,api_key)

events1= get(events_url)

#TODO: Print the entire response
print (json.dumps(events1, indent=4, sort_keys=True))

#TODO: Print the events where Malware executed. You will be using For loop to parse the json in the response
for events1 in events1["data"]:
    if events1["event_type_id"] == event_id:
        print(events1)
    else:
        continue
