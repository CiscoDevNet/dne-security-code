#!/usr/bin/env python
"""
Cisco Intro to AMP Hands on Exercisce Step2

Copyright (c) 2018-2020 Cisco and/or its affiliates.

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
from crayons import green, yellow
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
    host=env_lab.AMP.get("host"),
    client_id=env_user.AMP_CLIENT_ID,
    api_key=env_user.AMP_API_KEY,
):
    """Get a list of recent events from Cisco AMP."""
    print("\n==> Getting recent events from AMP")
    # TODO: Construct the URL
    url = f"https://{client_id}:{api_key}@{host}/v1/events"

    response = requests.get(url, verify=False)
    response.raise_for_status()

    events_list = response.json()["data"]
    
    return events_list


def write_events_to_file(filepath, ampevents):
    with open(events_path, "w") as file:
        json.dump(ampevents, file, indent=2)


# If this script is the "main" script, run...
if __name__ == "__main__":
    # TODO: Get the list of events from AMP
    # Hint: Call the function to get AMP events and assign it to variable amp_events
    
    # TODO: Print the total number of events observed. 
    print(yellow(f"Received total {len(amp_events)} malware events"))
    # Get the current file directory root
    repository_root = (here).resolve()
    # create a newfile "events.json" 
    events_path = repository_root / "events.json"
    # TODO: Store the events observed in a file. 
    # Hint: 1 set up path (uncomment next line)
    # events_path = repository_root / "events.json"

    print(green(f"\n==> Saving events to: {events_path}"))
    #TODO: Hint: 2 you can all the write_events_to_file function

