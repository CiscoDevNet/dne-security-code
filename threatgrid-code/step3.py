#!/usr/bin/env python
"""step3 - edit this file
This is your starting point for the 0day workflow  Mission.
Edit this file to
 -
There are a few places to edit (search for MISSION comments)
Script Dependencies:
    requests, json
Depencency Installation:
    $ pip install requests
    $ pip install json
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
import sys
# Disable SSL Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
#TODO: Enter the key provided by the DNE instructor or your own threatgrid api key
api_key = ''
#TODO: Enter the resource URL
url =''.format(api_key)
try:
    r = requests.get(url)
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        json_resp = json.loads(resp)

        resp2=json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': '))
        print(resp2)
        #TODO: Create a file save the token into a text file, Hint refer to the python example on previous page in lab

    else:
        r.raise_for_status()
        print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err))
finally:
    if r : r.close()
