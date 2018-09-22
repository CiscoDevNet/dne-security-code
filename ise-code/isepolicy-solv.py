#!/usr/bin/env python
"""isepolicy - edit this file
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
from datetime import datetime
import sys
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


#TODO: Enter all authentication info
ISE_ERSUSER="ersadmin"
ISE_ERSPASSWORD="C1sco12345"
ISE_HOSTNAME="198.18.133.27:9060"
#TODO: Get the ISE URL setup
url = "https://" + ISE_ERSUSER + ":" + ISE_ERSPASSWORD + "@" + ISE_HOSTNAME + "/ers/config/ancpolicy"
#Let's create content headers
headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }
namelist={}
#TODO:create the GET request 
response = requests.request("GET", url, verify=False, headers=headers)
if(response.status_code == 200):
    #TODO: Put the logic to parse the response to print the name of the ANC policies
    resp_json=response.json()
    for newlist in resp_json["SearchResult"]["resources"]:
        namelist=newlist["name"]
    print("Name of the ANC policy exits in system:",namelist)
else:
        print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})
