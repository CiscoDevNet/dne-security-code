#!/usr/bin/env python
"""Mission - SecureX Threat Response
Do threat research and investigations via SecureX threat response.
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
from datetime import datetime

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

username = "client-"
password = "a1b2c3d4"
ctr_observables="[{ \"value\": \"b1380fd95bc5c0729738dcda2696aa0a7c6ee97a93d992931ce717a0df523967\", \"type\": \"sha256\" }]"
host = "visibility.amp.cisco.com"

from env_user import WEBEX_TEAMS_ACCESS_TOKEN
from env_user import WEBEX_TEAMS_ROOM_ID
# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Step One: Create a function that provides your username and password from SecureX and returns an access token that will be used for API authorization.

def get_ctr_token():
    url = f"https://{host}/iroh/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    #TODO Insert the HTTP payload statement required to request the access token
    payload = #TODO 1.0 - Hint use Postman to find this
    try:
        response = requests.post(url, headers=headers, auth=(username, password), data=payload)
    except:
        response.raise_for_status()

    return(response.json()["access_token"])

# Step Two: Create a function that provides additional details about an observation (IOC).  Within SecureX Threat Response, this functionality is called enriching.

def enrich_observables(observables):

    token = get_ctr_token()
    url = f"https://{host}/iroh/iroh-enrich/deliberate/observables"
    headers = {'Content-Type': 'application/json',
                         'Accept': '*/*',
                         'Authorization': 'Bearer ' + token}
    #TODO Supply the variable that holds the CTR observables.  In this case it's included in this script, however it can also be supplied from a file or the result of another API call.
    payload = #TODO 2.0
    
    response = requests.post(url, headers=headers, data = payload)
    
    print(blue("==> Enrich Observables using SecureX threat response"))

    print(f"Observable: {response.json()['data'][0]['data']['verdicts']['docs'][0]['observable']['value']}")
    print(f"Type: {response.json()['data'][0]['data']['verdicts']['docs'][0]['observable']['type']}")
    print(f"Verdict: {response.json()['data'][0]['data']['verdicts']['docs'][0]['disposition_name']}")

# Step Three: Create a function that creates a new case in the SecureX threat response Casebook and adds our observables to it for a new invesigation.

def add_to_casebook():

    token = get_ctr_token()

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    casebook_title = "DNE Casebook"
    casebook_description = "Python generated casebook from DNE SecureX Mission"
    casebook_datetime = datetime.now().isoformat() + "Z"

    #TODO Replace the items below with variables generated within this function to properly format the JSON for creating a new case.
    casebook_json = json.dumps({
        "title": #TODO 3.0,
        "description": #TODO 3.1,
        "observables": json.loads(ctr_observables),
        "type": "casebook",
        "timestamp": #TODO 3.2
    })

    response = requests.post('https://private.intel.amp.cisco.com/ctia/casebook', headers=headers, data=casebook_json)

    print(blue("==> Creating new case to add to SecureX threat response Casebook"))

    if response.status_code == 201:
        print(green(f"[201] Success, case added to Casebook added with title {casebook_title}\n"))
    else:
        print(f"Something went wrong while posting the casebook to CTR, status code: {response.status_code}\n")

    return response.text

# Step 4: Call our functions for enrichment and adding a new case into the Casebook.

if __name__ == "__main__":
    
    #TODO Supply the function calls below to return the enrichment verdict and to add the observable to a new case.

    #TODO 4.0
    #Hint call the enrich function with the observables variable
    #TODO 4.1
    #Hint call the function to add a case to the casebook

    # Finally, post a message to the Webex Teams Room to brag!!!
    print(blue("\n==> Posting message to Webex Teams"))

    teams = webexteamssdk.WebexTeamsAPI(WEBEX_TEAMS_ACCESS_TOKEN)
    teams.messages.create(
        roomId=WEBEX_TEAMS_ROOM_ID,
        markdown=f"**SecureX threat response Mission completed!!!** \n\n"
                 f"I enriched an observable and added it to a Casebook."
    )