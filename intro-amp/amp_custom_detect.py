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

SAMPLE_SHA256="3372c1edab46837f1e973164fa2d726c5c7f17dcb888828ccd7c4dfcc234a375"

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Functions
def get_amp_detections(
    host=env_lab.AMP.get("host"),
    client_id=env_user.AMP_CLIENT_ID,
    api_key=env_user.AMP_API_KEY
):
    """Get a list of recent custom detections from Cisco AMP."""
    print("\n==> Getting recent custom detections from AMP")

    url = f"https://{client_id}:{api_key}@{host}/v1/file_lists/simple_custom_detections"

    response = requests.get(url, verify=False)
    response.raise_for_status()

    events_list = response.json()

    print(green(f"Retrieved {len(events_list)} data from AMP"))

    return events_list

def parseResponse(file_lists):
    print(file_lists)
    for item in file_lists["data"]:
        if item["name"] == "File Blacklist":
            list_id = item["guid"]
    return list_id
    
def post_to_amp(
    list_id,
    payload,
    host=env_lab.AMP.get("host"),
    client_id=env_user.AMP_CLIENT_ID,
    api_key=env_user.AMP_API_KEY):
    print("\n==> Adding  SHA to AMP custom detections list")

    url = f"https://{client_id}:{api_key}@{host}/v1/file_lists/{list_id}/files/{SAMPLE_SHA256}"

    response = requests.post(url, post_this, verify=False)
    response.raise_for_status()

    rdata = response.json()["data"]
    return rdata

# If this script is the "main" script, run...
if __name__ == "__main__":

    #TODO: Call the function to get detections
    dects = get_amp_detections()
    #TODO: Call the function to parse the custome detections list
    list_id = parseResponse(dects)
    post_this =  {'description':'created by DNE user using API'}
    #TODO: Call post function to add a problem sha to your custom detection list 
    response = post_to_amp(list_id, post_this)
    
    print(f"\n==> Successfully added {SAMPLE_SHA256} to AMP custom detections list")

