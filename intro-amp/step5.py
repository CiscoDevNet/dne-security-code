
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
# Disable SSL Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
#BONOS TODO: You can create the function definitions to do GET and POST operations

#main code
#TODO: ENTER YOU CLIENT ID AND API KEY HERE
client_id =
api_key =

#This is the SHA we will enter in the Blacklist of our AMP custom detection list.
#This information is generally validated with threat intelligence systems like Cisco ThreatGrid or Virustotal
sha_256="3372c1edab46837f1e973164fa2d726c5c5e17bcb888828ccd7c4dfcc234a375"

#TODO: Create the URL /v1/file_lists/simple_custom_detections is the api endpoint.

file_list_url = ""

#First do the GET request to find the custom blacklist file exists
response = requests.get(PUT_YOUR_URL_HERE, verify=False)



file_lists= response.json()

#TODO: Parse the response json, and find the "File Blacklist"
for item in file_lists["data"]:
    if item["name"] == "#TODO What will go here?":
        list_id = item["guid"]

#Create the payload to update the list with new SHA
post_this =  {'description':'created by DNE user using API'}

#TODO: Create the POST URL and Add sha to it
add_list_url = "https://{}:{}@amp.dcloud.cisco.com/v1/file_lists/{}/files/{}".format(client_id, api_key,list_id, ADD_THE_SHA_HERE)

#TODO: Now you have URL figured out, Do your POST to update the SHA in the blacklist.
response = requests.post(PUT_YOUR_URL_HERE, PUT_YOUR_DATA_HERE, verify=False)

print(response)
