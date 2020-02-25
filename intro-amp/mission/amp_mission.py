#!/usr/bin/env python
"""Mission - Cisco AMP

This is your starting point for the Zero-day Workflow.


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
from inspect import currentframe

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
def get_amp_events(
    host=env_lab.AMP.get("host"),
    client_id=env_user.AMP_CLIENT_ID,
    api_key=env_user.AMP_API_KEY,
):
    """Get a list of recent events from Cisco AMP."""
    print(blue("\n==> Getting recent events from AMP"))

    url = f"https://{client_id}:{api_key}@{host}/v1/events"

    response = requests.get(url, verify=False)
    response.raise_for_status()

    events_list = response.json()["data"]

    print(green(f"Retrieved {len(events_list)} events from AMP"))

    return events_list


def get_amp_computer_details( url,
    client_id=env_user.AMP_CLIENT_ID,
    api_key=env_user.AMP_API_KEY,
    ):

    """Get details of infected computer from Cisco AMP."""
    url = f"https://{client_id}:{api_key}@{url}"

    #TODO: do a GET request to retrieve infected computer details (remmeber to NOT do SSL verification!) 
    # Hint: Remember to assign it varibale "response"
    env_lab.print_missing_mission_warn(env_lab.get_line())

    response = MISSION
    response.raise_for_status()
    events_list = response.json()["data"]
    return events_list


def extract_observables(amp_events):
    """Extract hash, IP, and MAC address observables from Malware events."""
    print(blue("\n==> Extracting observables from the AMP events"))

    # Initialize data structures for collecting observables
    observables = []

    # Standard AMP event ID for Malware events
    malware_event_id = 1107296272
    value = ""
    ip = ""
    mac = ""
    sha256= ""
    for event in amp_events:
        if event["event_type_id"] == malware_event_id:
            try:
                hostname = event["computer"]["hostname"]
                """ get the links URL to get details of infected computer"""
                url = event["computer"]["links"]["computer"]
                malU=url.partition("https://")[2]

                """ get the links URL to get details of infected computer"""
                events_list = get_amp_computer_details(malU)
                ip = events_list["network_addresses"][0]["ip"]
                mac = events_list["network_addresses"][0]["mac"]
                sha256 = event["file"]["identity"]["sha256"]
                """ Handle missing dict Key errors"""
            except KeyError as ke:
                value = "None"
            observables.append({
                "hostname": hostname,
                "ip_address": ip,
                "mac_address": mac,
                "sha256": sha256,
            })

    if observables:
        print(green(f"Extracted observables from "
                    f"{len(observables)} malware events"))
    else:
        print(red("No malware events found."))
        sys.exit(1)

    return observables



# If this script is the "main" script, run...
if __name__ == "__main__":
    #TODO: Use the right function to fill the amp_events variable with the AMP events
    env_lab.print_missing_mission_warn(env_lab.get_line())
    amp_events = MISSION

    #TODO: Use the right function to fill the amp_observables variable with extracted observables from the AMP events
    env_lab.print_missing_mission_warn(env_lab.get_line())
    amp_observables = MISSION

    # Save the MAC addresses of the endpoints where malware executed to a JSON
    # file.  In the ISE Mission we will read this file and quarantine these
    # endpoints.
    mac_addresses_path = repository_root / "mission-data/mac-addresses.json"
    print(blue(f"\n==> Saving MAC addresses to: {mac_addresses_path}"))

    with open(mac_addresses_path, "w") as file:
        mac_addresses = [o["mac_address"] for o in amp_observables]
        json.dump(mac_addresses, file, indent=2)

    # Save the malware SHA256 hashes to a JSON file. We will use these in the
    # ThreatGrid Mission.
    sha256_list_path = repository_root / "mission-data/sha256-list.json"
    print(blue(f"\n==> Saving SHA256 hashes to: {sha256_list_path}"))

    #TODO: open a file and write to it, similar to the code in lines 154-156. However, this time use the sha256_list_path, and instead of mac addresses. use the sha256 hashes. (Tip: try to print amp_observables, so that you know what to search for.)
    env_lab.print_missing_mission_warn(env_lab.get_line())
    with open(MISSION, "w") as file:
        MISSION = [o["MISSION"] for o in amp_observables]
        json.dump(MISSION, file, indent=2)

    # Finally, post a message to the Webex Teams Room to brag!!!
    print(blue("\n==> Posting message to Webex Teams"))

    teams = webexteamssdk.WebexTeamsAPI(env_user.WEBEX_TEAMS_ACCESS_TOKEN)
    teams.messages.create(
        roomId=env_user.WEBEX_TEAMS_ROOM_ID,
        markdown=f"**AMP Mission completed!!!** \n\n"
                 f"I extracted observables from {len(amp_observables)} AMP "
                 f"malware events."
    )

    print(green("AMP Mission Completed!!!"))
