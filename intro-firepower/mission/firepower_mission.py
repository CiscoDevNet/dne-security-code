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

pathf = Path(__file__).parent.absolute()
fdmfolder = (pathf / ".." / "fdm").resolve()
from fdm_auth import fdm_login


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
        "password": password,
    }
    url = f"https://{host}:{port}/api/fdm/v1/fdm/token"
    r = requests.post(url, data=auth_payload, verify=False, headers=headers)
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
def create_url_object(client):
    url_object = client.get_model("URLObject")(type="urlobject")
    url_object.name = "DNEbadguys"
    #Mission TODO: Enter the domain you found malicious or questionable in Umbrella Investigate to block on FTD
    url_object.url = "internetbadguys.com"
    client.URLObject.addURLObject(body=url_object).result()


def create_access_rule(client):
    # get access policy first
    access_policy = client.AccessPolicy.getAccessPolicyList().result()['items'][0]
    # fetch the url object we created
    url_object = client.URLObject.getURLObjectList(filter="name:DNEbadguys").result()['items'][0]
    # reference model (name, id, type)
    ReferenceModel = client.get_model("ReferenceModel")

    # create embedded app filter
    embedded_url_filter = client.get_model("EmbeddedURLFilter")(type="embeddedurlfilter")
    embedded_url_filter.urlObjects = [ReferenceModel(id=url_object.id, type=url_object.type)]

    # Access Rule model
    access_rule = client.get_model("AccessRule")(type="accessrule")
    access_rule.name = "block_DNEbadguys"
    access_rule.urlFilter = embedded_url_filter
    client.AccessPolicy.addAccessRule(body=access_rule, parentId=access_policy.id).result()
    print(blue("\n==> Posting message to Webex Teams"))

    teams = webexteamssdk.WebexTeamsAPI(env_user.WEBEX_TEAMS_ACCESS_TOKEN)
    teams.messages.create(
        roomId=env_user.WEBEX_TEAMS_ROOM_ID,
        markdown=f"**Firepower - FDM Mission completed!!!** \n\n"
                 f"I was able to block domains {} "
                 
    )

    print(green("Firepower - FDM: Mission Completed!!!"))
    
    message = teams.messages.create(WEBEX_TEAMS_ROOM_ID,
    text='MISSION: 0day FDM Blocking the Domain URL - I have completed the mission!')
    #Mission TODO3: Print the responset 
    print(message)

if __name__ == '__main__':
    login()
    client = get_spec_json()
    create_url_object(client)
    create_access_rule(client)
