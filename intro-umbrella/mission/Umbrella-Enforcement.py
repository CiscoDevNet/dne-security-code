
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
SPARK_ROOM_ID = ""

spark = ciscosparkapi.CiscoSparkAPI(SPARK_ACCESS_TOKEN)
# import necessary libraries / modules
import requests
from datetime import datetime
import json

#Mission TODO2: copy paste API key from previous section within the quotes
custkey = ""

# URL needed to do POST requests
eventurl = "https://s-platform.api.opendns.com/1.0/events"
# time for AlertTime and EventTime when domains are added to Umbrella

time = datetime.now().isoformat() 

# domain that will be uploaded
domain = "hjhqmbxyinislkkt.1j9r76.top"

# URL needed for POST request
UrlPost = eventurl+'?customerKey='+custkey

# NOTE: Although this information MUST be provided when using the API, not all of it is utilized in the destination lists within Umbrella
data = {
      "alertTime": time + "Z",
      "deviceId": "ba6a59f4-e692-4724-ba36-c28132c761de",
      "deviceVersion": "13.7a",
      "dstDomain": domain,
      "dstUrl": "http://" + domain + "/",
      "eventTime": time + "Z",
      "protocolVersion": "1.0a",
      "providerName": "Security Platform"
}

# POST REQUEST: post request ensembly
req = requests.post(UrlPost, data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
# error handling if true then the request was HTTP 202, so successful 
if(req.status_code == 202):
    print("SUCCESS: domain (%(domain)s) was accepted, HTTP response: 202, timestamp: %(time)s" % {'domain': domain, 'time': time})
    message = spark.messages.create(SPARK_ROOM_ID,text='MISSION: 0day Umbrella-Enforcement - I have completed the first mission!')
    print(message)
else:
    print("An error has ocurred with the following code %(error)s, please consult the following link: https://enforcement-api.readme.io/" % {'error': req.status_code})
