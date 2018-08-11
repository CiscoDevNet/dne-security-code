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

ISE_ERSUSER="ersadmin"
ISE_ERSPASSWORD="C1sco12345"
ISE_HOSTNAME="198.18.133.27:9060"

url = "https://" + ISE_ERSUSER + ":" + ISE_ERSPASSWORD + "@" + ISE_HOSTNAME + "/ers/config/endpoint"

print(url)
#:C1sco12345@198.18.133.27:9060/ers/config/ancpolicy"

headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

response = requests.request("GET", url, verify=False, headers=headers)
if(response.status_code == 200):
     message = spark.messages.create(SPARK_ROOM_ID,
	 text='MISSION: 0day ISE - I have completed the first mission to get the ISE Endpoint!')
    #Mission TODO3: Print the response
    print("Done!...Mission part 1 getting endpoint")
else:
        print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})


url = "https://" + ISE_ERSUSER + ":" + ISE_ERSPASSWORD + "@" + ISE_HOSTNAME + "/ers/config/ancendpoint/apply"

payload = "{\r\n    \"OperationAdditionalData\": {\r\n    \"additionalData\": [{\r\n    \"name\": \"macAddress\",\r\n    \"value\": \"11:22:33:44:55:66\"\r\n    },\r\n    {\r\n    \"name\": \"policyName\",\r\n    \"value\": \"ANC_Devnet\"\r\n    }]\r\n  }\r\n}"


print (url)
response = requests.request("PUT", url, data=payload, verify=False, headers=headers)
if(response.status_code == 204):
     message = spark.messages.create(SPARK_ROOM_ID,
	 text='MISSION: 0day ISE - I have completed the first mission to get the ISE Endpoint!')
    #Mission TODO3: Print the response
    print("Done!...Mission part 2 applying Quarantine policy to the rouge endpoint")
else:
    print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})