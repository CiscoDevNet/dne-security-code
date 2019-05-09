#!/usr/bin/env python
"""


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

from datetime import datetime
import requests
import socket
import configparser
import json
import sys
from pathlib import Path
import webexteamssdk
from crayons import blue, green, red
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / "..").resolve()

sys.path.insert(0, str(repository_root))

sys.path.insert(0, str(repository_root))

from env_lab import UMBRELLA  # noqa
from env_user import UMBRELLA_ENFORCEMENT_KEY
from env_user import UMBRELLA_INVESTIGATE_KEY  # noqa
from env_user import WEBEX_TEAMS_ACCESS_TOKEN
from env_user import WEBEX_TEAMS_ROOM_ID
# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

enforcement_api_key = UMBRELLA_ENFORCEMENT_KEY

time = datetime.now().isoformat()


# URL needed to do POST requests
event_url = "https://s-platform.api.opendns.com/1.0/events"

# time for AlertTime and EventTime when domains are added to Umbrella
time = datetime.now().isoformat()

# domain that will be uploaded
domain = "internetbadguys.com"

# URL needed for POST request
url_post = event_url+'?customerKey='+ enforcement_api_key

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
req = requests.post(url_post, data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})

# error handling if true then the request was HTTP 202, so successful
if(req.status_code == 202):
    print("SUCCESS: domain (%(domain)s) was accepted, HTTP response: 202, timestamp: %(time)s" % {'domain': domain, 'time': time})
else:
    print("An error has ocurred with the following code %(error)s, please consult the following link: https://enforcement-api.readme.io/" % {'error': req.status_code})
