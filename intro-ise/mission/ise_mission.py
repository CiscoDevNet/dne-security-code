#!/usr/bin/env python
"""Mission - Cisco ISE

Copyright (c) 2018-2019 Cisco and/or its affiliates.

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
import json
import sys
from pathlib import Path

import requests
import webexteamssdk
from crayons import blue, green, red
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))

import env_lab  # noqa
import env_user  # noqa


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Functions

def createPayload(maclist, policy):
    data_to_send = {
        'OperationAdditionalData': {
            'additionalData' : [{
                'name': 'macAddress',
                f'value': maclist
                },
                {
                    'name': 'policyName',
                    f'value': policy
                    }]
        }
    }
    return data_to_send


def readmacaddr_file(filename) :
    with open (filename, 'r') as fp:
        maclist = json.loads(fp.read())
    return maclist

headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }
username = env_lab.ISE.get("username")
password = env_lab.ISE.get("password")
host = env_lab.ISE.get("host")
port = env_lab.ISE.get("port")


def get_policy_ise():

    #TODO: Create the URL for the GET request to get the ANC policy from ISE. Hint: Make sure you pass the Auth paramenters for the API call
    env_lab.print_missing_mission_warn(env_lab.get_line())
    url = MISSION

    #Create GET Request
    req = requests.get(url, verify=False, headers=headers)
    #req = requests.request("GET", url, verify=False, headers=headers)
    namelist = " "
    if(req.status_code == 200):
        resp_json = req.json()
        policies = resp_json["SearchResult"]["resources"]
        for policy in policies:
            namelist = policy["name"]
            print("\nI've Found the Quarantine Policy {0} to Nuke the Rogue computers from the corp network... \n".format(namelist) )
    else:
        print("An error has ocurred with the following code %(error)s" % {'error': req.status_code})
    return namelist

def post_to_ise(maclist, namelist):
    #TODO: Create the URL for the PUT request to apply the ANC policy! Hint: Make sure you pass the Auth paramenters for the API call
    url = MISSION
    env_lab.print_missing_mission_warn(env_lab.get_line())
    
    for items in maclist:
        payload = "{\r\n    \"OperationAdditionalData\": {\r\n    \"additionalData\": [{\r\n    \"name\": \"macAddress\",\r\n    \"value\": \""+ items + "\"\r\n    },\r\n    {\r\n    \"name\": \"policyName\",\r\n    \"value\": \"" + namelist + '"' + "\r\n    }]\r\n  }\r\n}"
        print(json.dumps(payload,sort_keys=True,indent=3))
        response = requests.request("PUT", url, data=payload, verify=False, headers=headers)
        if(response.status_code == 204):
            print("Done!..Applied Quarantine policy to the rogue endpoint...MAC: {0} Threat is now contained....".format(items))
        else:
            print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})

if __name__ == "__main__":
   maclist_path = repository_root / "mission-data/mac-addresses.json"
   maclist = readmacaddr_file(maclist_path)

   #TODO Call the function for getting ANC policy and store it in the policylist variable
   env_lab.print_missing_mission_warn(env_lab.get_line())
   policylist = MISSION

   #TODO call the function for applying policy to the endpoints
   env_lab.print_missing_mission_warn(env_lab.get_line())

   # # Finally, post a message to the Webex Teams Room to brag!!!
   print(blue("\n==> Posting message to Webex Teams"))
   teams = webexteamssdk.WebexTeamsAPI(env_user.WEBEX_TEAMS_ACCESS_TOKEN)
   teams.messages.create(
       roomId=env_user.WEBEX_TEAMS_ROOM_ID,
       markdown=f"**ISE Mission completed!!!** \n\n"
       f"I have applied quarantine policy to the rogue endpoints! \n\n"

   )

   print(green("ISE Mission Completed!!!"))
