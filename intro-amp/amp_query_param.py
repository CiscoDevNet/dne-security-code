#!/usr/bin/env python
"""
Intro to Cisco AMP Step 3 
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
repository_root = (here / ".." ).resolve()

sys.path.insert(0, str(repository_root))

import env_lab  # noqa
import env_user  # noqa


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Functions
def get_amp_events(
    qparams,
    host=env_lab.AMP.get("host"),
    client_id=env_user.AMP_CLIENT_ID,
    api_key=env_user.AMP_API_KEY
):
    """Get a list of recent events from Cisco AMP."""
    print("\n==> Getting recent events from AMP")

    url = f"https://{client_id}:{api_key}@{host}/v1/events"

    response = requests.get(url,params=qparams, verify=False)
    response.raise_for_status()

    events_list = response.json()["data"]

    print(green(f"Retrieved {len(events_list)} events from AMP"))

    return events_list


# If this script is the "main" script, run...
if __name__ == "__main__":
    #TODO: Create the query for AMP here 
    #Hint: create a variable qparams  and assign "event_type[]=1090519054&limit=10" to it
    qparams =   
    #TODO: Call the function to get events
    #Hint : Call the correct function and assign return value to a variable "amp_events"
    amp_events =
    #TODO: Print the events (Think if you can make a colored print like previous examples)
    print(json.dumps(MISSION, indent=2))

