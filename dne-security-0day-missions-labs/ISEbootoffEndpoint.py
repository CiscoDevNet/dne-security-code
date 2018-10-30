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

# Mission TO DO2: Get the ISE URL setup

ISE_ERSUSER=
ISE_ERSPASSWORD=
ISE_HOSTNAME=

# Mission Note: You have nothing to do here. But remember this information will come from the AMP (The MAC address of rouge endpoints)
# currently have only one endpoint registered with ISE in DNE dcloud pod, hence we will use this information only. But in your network
# you can automate this . AMP provides rouge/malicious endpoints MAC address and you Quarantine them using ISE ANC policy
ISE_ENDPOINT="11:22:33:44:55:66"

#Mission TODO 4: Create URL to Get the ANC policy : Hint you have already done this exercise in ISE DNE module
url = "MISSION"


headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

response = requests.request("GET", url, verify=False, headers=headers)

#Mission TODO 5: Parse and store your policy in this variable.
namelist={}
if(response.status_code == 200):
    resp_json = response.json()
    #Mission TODO 6: Parse the json dict using for loop to get Policy name and assign it to "namelist"
    message = spark.messages.create(SPARK_ROOM_ID,
    text='MISSION: 0day ISE - I have completed the first mission to get the ISE Policy!')
    #Mission TODO3: Print the response policy name you parsed

    print(namelist)
    print("Done!...Mission part 1 getting endpoint")
else:
        print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})

#Mission TODO 7: Create url to apply policy use this endpoint /ers/config/ancendpoint/apply
url =

#Mission TODO 8: Update the payload with policy name variable you used to parse and store in TODO #6 hint "namelist"
payload = "{\r\n    \"OperationAdditionalData\": {\r\n    \"additionalData\": [{\r\n    \"name\": \"macAddress\",\r\n    \"value\": \""+ ISE_ENDPOINT + "\"\r\n    },\r\n    {\r\n    \"name\": \"policyName\",\r\n    \"value\": \""+ TODO_UPDATE_ME+ '"' + "\r\n    }]\r\n  }\r\n}"

#you can uncomment these line to quickly check you payload. If payload is not correct ISE will return 400 status code
#print(payload)
#print(url)

response = requests.request("PUT", url, data=payload, verify=False, headers=headers)
if(response.status_code == 204):
    message = spark.messages.create(SPARK_ROOM_ID,
    text='MISSION: 0day ISE - I have completed the first mission to get the ISE Endpoint!')
    #Mission TODO 9: Print the response
    print("Done!...Mission part 2 applying Quarantine policy to the rouge endpoint")
else:
    print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})
