#!/usr/bin/env python
"""
FDM Mission --- Now you will apply the URL filtering on the NGFW.

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
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient

# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))


from env_lab import FDM
from env_user import WEBEX_TEAMS_ACCESS_TOKEN
from env_user import WEBEX_TEAMS_ROOM_ID
pathf = Path(__file__).parent.absolute()
fdmfolder = (pathf / ".." / "fdm").resolve()


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer "
}

#mission TODO: Enter the FTD hostname/ip here... (TIP: dont't forget to use HTTPS + the IP)

def login(host=FDM.get("host"),
    port=FDM.get("port"),
    username=FDM.get("username"),
    password=FDM.get("password"),):
    
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password
    }
    url = f"https://{host}:{port}/api/fdm/v1/fdm/token"
    print (url)
    print (payload)
    r = requests.post(url, json=payload, verify=False, headers=headers)
    print(r)
    access_token = "Bearer %s" % r.json()['access_token']
    headers['Authorization'] = access_token

def get_spec_json(host=FDM.get("host"),
    port=FDM.get("port"),
    username=FDM.get("username"),
    password=FDM.get("password"),):
    http_client = RequestsClient()
    http_client.session.verify = False
    http_client.session.headers = headers
    url = f"https://{host}:{port}/apispec/ngfw.json"
    client = SwaggerClient.from_url(url, http_client=http_client, config={'validate_responses':False})
    return client

# ----------------
def create_url_object(client, domains):
    url_object = client.get_model("URLObject")(type="urlobject")
    url_object.name = domains
    #Mission TODO: Enter the domain you found malicious or questionable in Umbrella Investigate to block on FTD
    url_object.url = domains
    client.URLObject.addURLObject(body=url_object).result()
    print(f"Created URL Object : {domains}\n\n")


def create_access_rule(client, domains):
    # get access policy first
    access_policy = client.AccessPolicy.getAccessPolicyList().result()['items'][0]
    # fetch the url object we created
    url_object = client.URLObject.getURLObjectList(filter=domains).result()['items'][0]
    # reference model (name, id, type)
    ReferenceModel = client.get_model("ReferenceModel")

    # create embedded app filter
    embedded_url_filter = client.get_model("EmbeddedURLFilter")(type="embeddedurlfilter")
    embedded_url_filter.urlObjects = [ReferenceModel(id=url_object.id, type=url_object.type)]

    # Access Rule model
    access_rule = client.get_model("AccessRule")(type="accessrule")
    access_rule.name = domains
    access_rule.urlFilter = embedded_url_filter
    access_rule.ruleAction = "DENY"
    client.AccessPolicy.addAccessRule(body=access_rule, parentId=access_policy.id).result()
    print(f"Created Access Policy to block URL Object : {domains}\n\n")

        
def removeDups(list) :
    domain_list_r = []
    domin_filter_ip = []
    domain_final = []
    for i in list:
        if i not in domain_list_r:
            domain_list_r.append(i)
            domain_filter_ip = domain_list_r
    print("We found dulicates and pruned the list :\n")
    return domain_filter_ip


def readdomains_file(filename) :
    with open (filename, 'r') as fp:
        maclist = json.loads(fp.read())
    return maclist


if __name__ == '__main__':
    #TODO Mission login for API access
    login()
    client = get_spec_json()
    domain_list = []
    clean_domains = []
    #Read the domain file created by ThreatGrid
    domainlist_path = repository_root / "mission-data/riskydomains.json"
    domain_list = readdomains_file(domainlist_path)
    #TODO Mission make sure there no duplicate domains
    clean_domains = removeDups(domain_list)
    #TODO Mission itrate through the domain list and create URL objects and rules
    for doms in clean_domains:
        create_url_object(client, doms)
        create_access_rule(client, doms)
    #post Message to WebEx Teams!
    print(blue("\n==> Posting message to Webex Teams"))
    teams = webexteamssdk.WebexTeamsAPI(WEBEX_TEAMS_ACCESS_TOKEN)
    teams.messages.create(
        roomId=WEBEX_TEAMS_ROOM_ID,
        markdown=f"**Firepower - FDM Mission completed!!!** \n\n"
                 f"I was able to block domains from the file"

    )
    print(green("Firepower - FDM: Mission Completed!!!"))
