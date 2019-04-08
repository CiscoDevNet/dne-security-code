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
import requests
import json
from datetime import datetime
import sys
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

#Mission TODO1: Please add your SPARK_ACCESS_TOKEN and SPARK_ROOM_ID here
SPARK_ACCESS_TOKEN = ""
SPARK_ROOM_ID=""

spark = ciscosparkapi.CiscoSparkAPI(SPARK_ACCESS_TOKEN)
# Mission TODO2: Insert the API key
APIkey = ""

# Mission TODO3: Insert the proper URL
investigateUrl = "https://investigate.api.umbrella.com/domains/categorization/"

# Mission TODO3: What is the domain that will be checked?
domain = "hjhqmbxyinislkkt.1j9r76.top"

# time for timestamp of verdict domain
time = datetime.now().isoformat()

#create header for authentication
headers = {
    'Authorization': 'Bearer ' + APIkey
    }

# assemble the URI, show labels give readable output
getUrl = investigateUrl + domain + "?showLabels"
print(getUrl)
# do GET request for the domain status and category
req = requests.get(getUrl, headers=headers)

# error handling if true then the request was HTTP 200, so successful
if(req.status_code == 200):
    # retrieve status for domain
    output = req.json()
    domainOutput = output[domain]
    # Mission TODO4: Parse the proper element in the response json
    domainStatus = domainOutput["status"]
    #walk through different options of status
if(domainStatus == -1):
    print("SUCCESS: The domain %(domain)s is found MALICIOUS at %(time)s" % {'domain': domain, 'time': time})
    message = spark.messages.create(SPARK_ROOM_ID,
    text='MISSION: 0day Umbrella-Investigate - I have completed the Umbrella Investigate mission!')
    print(message)
elif(domainStatus == 1):
    print("SUCCESS: The domain %(domain)s is found CLEAN at %(time)s" % {'domain': domain, 'time': time})
elif(domainStatus==0):
    print("SUCCESS: The domain %(domain)s is found UNDEFINED / RISKY at %(time)s" % {'domain': domain, 'time': time})
else:
    print("An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" % {'error': req.status_code})
