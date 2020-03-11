#!/usr/bin/env python
"""Mission - Cisco Umbrella

This is your research step in the Zero-day Workflow.


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
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))

import env_lab
from env_lab import UMBRELLA  # noqa
from env_user import UMBRELLA_ENFORCEMENT_KEY
from env_user import UMBRELLA_INVESTIGATE_KEY  # noqa
from env_user import WEBEX_TEAMS_ACCESS_TOKEN
from env_user import WEBEX_TEAMS_ROOM_ID
# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            #print(address)
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

# Read the config file to get settings

enforcement_api_key = UMBRELLA_ENFORCEMENT_KEY

time = datetime.now().isoformat()

investigate_api_key = UMBRELLA_INVESTIGATE_KEY




# URL needed to do POST requests
event_url = UMBRELLA.get("en_url")

# URL needed for POST request
url_post = event_url + '?customerKey=' + enforcement_api_key

inv_u = UMBRELLA.get("inv_url")

#TODO: finish the URL to get the Status and Category of a domain!
env_lab.print_missing_mission_warn(env_lab.get_line())
investigate_url = MISSION

#create header for authentication and set limit of sample return to 1
headers = {
'Authorization': 'Bearer ' + investigate_api_key,
'limit': '1'
}
#print(url_post)

def get_DomainStatus(getUrl, domain):
    #print(getUrl)
    req = requests.get(getUrl, headers=headers)
    if(req.status_code == 200):
        output = req.json()
        domainOutput = output[domain]
        domainStatus = domainOutput["status"]
        if(domainStatus == -1):
            print("SUCCESS: The domain %(domain)s is found MALICIOUS at %(time)s" %
            {'domain': domain, 'time': time})
            return "bad"
        elif(domainStatus == 1):
            #print("SUCCESS: The domain %(domain)s is found CLEAN at %(time)s" %
            #{'domain': domain, 'time': time})
            return "clean"
        #TODO: check if else the domain status is risky
        elif(MISSION):
            print(MISSION)
            return "MISSION"
    else:
        print("An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" %
          {'error': req.status_code})
        return "error"

def readIocsFile(filename):
    with open (filename, 'r') as fp:
        shalist = json.loads(fp.read())
    return shalist

def write_risky_domains_for_firewall(filenamed, domainlist):
    with open(filenamed, "w") as file:
        json.dump(domainlist, file, indent=2)

def removeDups(list):
    domain_list_r = []
    domin_filter_ip = []
    domain_final = []
    for i in list:
        if i not in domain_list_r:
            domain_list_r.append(i)
            domain_filter_ip = domain_list_r
    print("We found dulicates and pruned the list :\n")
    return domain_filter_ip

def handleDomains(filename):
    try:
        domain_list = readIocsFile(filename)
        time = datetime.now().isoformat()
        domain_list_f = []

        #TODO: call the correct function to remove duplicate domains from the domain list
        domain_list = MISSION
        env_lab.print_missing_mission_warn(env_lab.get_line())
        #TODO: loop through every domain in the domain list HINT: for ... in ...:
        for MISSION in MISSION:
            print(f"Working on {MISSION} .....")
            get_url = investigate_url + MISSION +  "?showLabels"
            status = get_DomainStatus(get_url, MISSION)
            if(status != "error"):
                if ((status == "bad") or (status == "risky")):
                    post_Enforcement(MISSION)
                    domain_list_f.append(MISSION)
                else:
                    print(f"Found clean domain, ignoring enforcement on {MISSION}")
            else:
                print("got error from Umbrella investigate")
        #Let's save another file with Umbrella Disposition on Domains
        # so that we block only bad & risky domains on firewalls
        filenamed = repository_root / "mission-data/riskydomains.json"
        write_risky_domains_for_firewall(filenamed, domain_list_f)
    except KeyboardInterrupt:
        print("\nExiting...\n")

def post_Enforcement(domdata):
    data={
                "alertTime": time + "Z",
                "deviceId": "ba6a59f4-e692-4724-ba36-c28132c761de",
                "deviceVersion": "13.7a",
                "dstDomain": domdata,
                "dstUrl": "http://" + domdata + "/",
                "eventTime": time + "Z",
                "protocolVersion": "1.0a",
                "providerName": "Security Platform"
    }
    request_post = requests.post(url_post, data=json.dumps(data), headers={
                                             'Content-type': 'application/json', 'Accept': 'application/json'})
    if(request_post.status_code == 202):
        print("\n")
        print(f"SUCCESS: {domdata} BLOCKED!!")
        print("\n")
    # error handling
    else:
        print("An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" %
                          {'error': request_post.status_code})


if __name__ == "__main__":
    # Save the MAC addresses of the endpoints where malware executed to a JSON
    # file.  In the ISE Mission we will read this file and quarantine these
    # endpoints.sha256-list.json
    domainlist_path = repository_root / "mission-data/domainlist.json"

    # TODO: Mission call the function to handle domains
    MISSION(domainlist_path)

    #TODO: initialize the teams object with the webexteamssdk using your access token and the ROOM_ID
    
    teams.MISSION(
        roomId=MISSION
        markdown=f"**Umbrella Mission completed!!!** \n\n"
                 f"I checked the status of the domains generated by ThreatGrid using Umbrella Investigate! \n\n"
                 f"I also blocked DNS lookup using Umbrella Enforcement API for Malicious and Risky Domains"

    )

    print(green("Umbrella Mission Completed!!!"))
