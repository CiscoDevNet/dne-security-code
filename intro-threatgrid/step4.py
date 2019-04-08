#!/usr/bin/env python
"""step4 - edit this file
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
#TODO: Enter the API Key provided by DNE instructor or use your own threatgrid api key
api_key = ''

#TODO: Enter from the example given in the learning lab
SHA256 = ''

#TODO: Enter the request URL, Hint please refer to the intro-threat-grid-api learning lab
url =''.format(api_key)
try:
    r = requests. #TODO enter the right GET method call on requests. Please refer to other code files in this repo
    #print (r.json())
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        json_resp = json.loads(resp)
        resp2=json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': '))
        print(resp2)
        #save the token into a text file
        fh = open("resultat-step4.txt", "w")
        #TODO Now enter the step to write the contents in the file..
        fh.close()
    else:
        r.raise_for_status()
        print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err))
finally:
    if r : r.close()
