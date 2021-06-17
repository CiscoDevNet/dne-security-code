#!/usr/bin/env python
"""Mission - Cisco ThreatGrid

This is your research step in the Zero-day Workflow.


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

from env_lab import THREATGRID  # noqa
from env_user import THREATGRID_API_KEY  # noqa
from env_user import WEBEX_TEAMS_ACCESS_TOKEN
from env_user import WEBEX_TEAMS_ROOM_ID
# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
th_headers = {
    'Content-Type': 'application/json'
    }
#Containers for the domains
domain_list = []
#containers for the Ips
ip_list = []
observables=[]
def readIocsFile(filename):
    with open (filename, 'r') as fp:
        shalist = json.loads(fp.read())
    return shalist

# step one query threatgrid for the sha_256 and extract relevant information
# important info is sample id
# import info is threat_score


def get_FromThreatGrid(path,
                       host=THREATGRID.get("host"),
                       key=THREATGRID_API_KEY,):
    """GET method for Threatgrid."""
    url = f"{host}/api/v2"
    response = requests.get(
        "https://{}{}&api_key={}".format(url, path, key),
        headers=th_headers
    )
    #print (response.json())
    # Consider any status other than 2xx an error
    response.raise_for_status()
    return response.json()


def find_Obervables(sha_256_1):
    print(f"Picking up the next sha from the list: {sha_256_1} ")
    samples = get_FromThreatGrid("/search/submissions?q={}".format(sha_256_1))
    #print (samples)
    if(samples == None):
        return
    if (samples == "Response [408]"):
        return
    sample_ids = {}
    behaviors = []
    flist_path = repository_root / "mission-data" / f"{sha_256_1}.json"
    for sample in samples['data']['items']:
        sample_ids[sample["item"]["sample"]
                   ] = sample["item"]["analysis"]["threat_score"]
        for behavior in sample["item"]["analysis"]["behaviors"]:
            behaviors.append(behavior["title"])
# Prepare TG report to screen with average score after number of runs and behavior
    behaviors = set(behaviors)
    num_of_runs = len(sample_ids)
    total = 0
    sample_string = ""
    domains = ""
    writeme=[]
    for sample, score in sample_ids.items():
        total = total + score
        sample_string = "{}{},".format(sample_string, sample)
    if(num_of_runs>0):
        print(f"Threat Score of sample: {total/num_of_runs}\n")
    else:
        print(f"Sample not found in the time window provided\n")
    for value in behaviors:
        if len(value)== 0:
            writeme.append(f"Sample for {sha_256_1} not found in the ThreatGrid.. Try increasing the time window or upload the sample")
        else:
            writeme.append(value)
        sample_string = sample_string[:-1]
    writer_file(flist_path, writeme, None)
    #print (sample_string)
    if len(sample_string) != 0:
        domains = get_FromThreatGrid(
            "/samples/feeds/domains?sample={}&after=2018-2-2".format(sample_string)) # if no samples returned, increase range, e.g. check out after 2010-07-18T21:39:13Z
        if (domains == "Response [408]"):
            return
        else:
            for domain in domains["data"]["items"]:
                if domain["relation"] == "dns-lookup":
                    for item in domain["data"]["answers"]:
                        observables.append({
                            "domains": domain["domain"],
                            "ip_address": item,
                        })

def writer_file(filename, glist, ioc):
    with open(filename, "w") as file:
        if ioc==None:
            json.dump(glist, file, indent=2)
        else:
            jsondata = [o[ioc] for o in glist]
            json.dump(jsondata, file, indent=2)
    file.close()



if __name__ == "__main__":
    # Save the MAC addresses of the endpoints where malware executed to a JSON
    # file.  In the ISE Mission we will read this file and quarantine these
    # endpoints.sha256-list.json
    shalist_path = repository_root / "mission-data/sha256-list.json"
    shalist = readIocsFile(shalist_path)
    #TODO: iterate through the shalist and find the observables per sha! hint: for ... in ...:
    env_lab.print_missing_mission_warn(env_lab.get_line())


    #Create data files for the Umbrella Mission.
    domainlist_path = repository_root / "mission-data/domainlist.json"
    iplist_path = repository_root / "mission-data/iplist.json"

    writer_file(domainlist_path, observables, "domains")

    #TODO: Write the ipaddress from observables to a file: Hint look above how we did the domains
    env_lab.print_missing_mission_warn(env_lab.get_line())
    writer_file(TODO)

    # Finally, post a message to the Webex Teams Room to brag!!!
    print(blue("\n==> Posting message to Webex Teams"))

    teams = webexteamssdk.WebexTeamsAPI(WEBEX_TEAMS_ACCESS_TOKEN)
    teams.messages.create(
        roomId=WEBEX_TEAMS_ROOM_ID,
        markdown=f"**ThreatGrid Mission completed!!!** \n\n"
                 f"I extracted domains & IP associated with SHAs {len(observables)} using ThreatGrid "
                 f"APIs Sample Search."
    )
