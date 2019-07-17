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

api_version = FDM.get("api_version")




def login(host=FDM.get("host"),
    port=FDM.get("port"),
    username=FDM.get("username"),
    password=FDM.get("password"), ):

    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    #mission TODO: Complete the URL to get FDM oAuth token Here is starting string "https://{host}:{port}/api/fdm/v{api_version}"
    env_lab.print_missing_mission_warn(env_lab.get_line())

    r = requests.post(url, json=payload, verify=False, headers=headers)
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
def create_reference_model(client, model):
    """
    Creates a ReferenceModel object referring to the passed in model object.
    This is used when one object refers to another object.

    client -- Bravado client object
    model -- destination model object
    """
    ReferenceModel = client.get_model('ReferenceModel')
    reference_model = ReferenceModel(id=model['id'], type=model['type'])
    if hasattr(model, 'name'):
        reference_model['name'] = model['name']
    if hasattr(model, 'version'):
        reference_model['version'] = model['version']
    return reference_model


def create_url_object(client, domain):
    """
    Creates a single URL object

    client -- Bravado client object
    domain -- A single domain to create into a URL object

    Return created URL object
    """
    url_object = client.get_model("URLObject")(type="urlobject")
    url_object.name = domain
    url_object.url = domain
    temp = client.URLObject.addURLObject(body=url_object).result()
    print(f"Created URL Object : {domain}\n\n")
    return temp

def create_url_object_group(client, name, url_objects):
    """
    Creates a single URL object group

    client -- Bravado client object
    name -- Name of the url object group
    url_objects -- List of URL objects to add to the group

    Returns single URL object group
    """
    url_object_group = client.get_model("URLObjectGroup")(type="urlobjectgroup")
    url_object_group.name = name
    url_object_group.objects = [create_reference_model(client, x) for x in url_objects]
    temp = client.URLObject.addURLObjectGroup(body=url_object_group).result()
    print(f"Created URL Group Object : {name}\n\n")
    return temp


def create_access_rule(client, url_object_group):
    """
    Creates a single access rule denying the url object group

    client -- Bravado client object
    url_object_group -- A single URL object group

    Returns created access rule
    """
    # get access policy first
    access_policy = client.AccessPolicy.getAccessPolicyList().result()['items'][0]

    # create embedded app filter
    embedded_url_filter = client.get_model("EmbeddedURLFilter")(type="embeddedurlfilter")
    embedded_url_filter.urlObjects = [create_reference_model(client, url_object_group)]

    # Access Rule model
    access_rule = client.get_model("AccessRule")(type="accessrule")
    access_rule.name = 'block bad domains'
    access_rule.urlFilter = embedded_url_filter
    access_rule.ruleAction = "DENY"
    temp = client.AccessPolicy.addAccessRule(body=access_rule, parentId=access_policy.id).result()
    print(f"Created Access Policy to block URL Object : {access_rule.name}\n\n")
    return temp

def dedupe_list(mylist) :
    """
    Creates a list without duplicates

    mylist -- The input list

    Returns List without the duplicates
    """
    deduped_items = []
    duplicates = []
    for i in mylist:
        if i not in deduped_items:
            deduped_items.append(i)
        else:
            duplicates.append(i)
            print(f"We found dulicates and pruned the list : {duplicates}\n")
    return deduped_items


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
   env_lab.print_missing_mission_warn(env_lab.get_line()) 

    url_objects = []
    for doms in clean_domains:
        url_objects.append(create_url_object(client, doms))

    #TODO Mission create a url group using the url_objects created in the above steps :
    #Pass these 3 values to the proper function client, "your_picked_name_for_URL_Object", url objects create in above for loop
    env_lab.print_missing_mission_warn(env_lab.get_line())

    #TODO Mission Create Access Rule to the block the URL object created above ... which will block all the risky domains
    env_lab.print_missing_mission_warn(env_lab.get_line())

    #post Message to WebEx Teams!
    print(blue("\n==> Posting message to Webex Teams"))
    teams = webexteamssdk.WebexTeamsAPI(WEBEX_TEAMS_ACCESS_TOKEN)
    teams.messages.create(
        roomId=WEBEX_TEAMS_ROOM_ID,
        markdown=f"**Firepower - FDM Mission completed!!!** \n\n"
                 f"I was able to block domains from the file"

    )
    print(green("Firepower - FDM: Mission Completed!!!"))
