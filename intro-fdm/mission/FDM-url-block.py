
"""0day Workflow Mission - edit this file
This is your starting point for the 0day workflow  Mission.
Edit this file to
 -
There are a few places to edit (search for MISSION comments)

Script Dependencies:
    requests
Depencency Installation:
    $ pip install requests
Copyright (c) 2018, Cisco Systems, Inc. All rights reserved.
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
import ciscosparkapi
import requests
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
#Mission TODO1: Please add your SPARK_ACCESS_TOKEN and SPARK_ROOM_ID here
SPARK_ACCESS_TOKEN = ""
SPARK_ROOM_ID=""

spark = ciscosparkapi.CiscoSparkAPI(SPARK_ACCESS_TOKEN)
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer "
}
#Mission TODO: Enter the FTD API access credentials here
auth_payload = '''
{
  "grant_type": "password",
  "username": "admin",
  "password": ""
}
'''

#mission TODO: Enter the FTD hostname/ip here... (TIP: dont't forget to use HTTPS + the IP)

hostname = ""

def login():
    r = requests.post(hostname + "/api/fdm/v1/fdm/token", data=auth_payload, verify=False, headers=headers)
    access_token = "Bearer %s" % r.json()['access_token']
    headers['Authorization'] = access_token

def get_spec_json():
    http_client = RequestsClient()
    http_client.session.verify = False
    http_client.session.headers = headers

    client = SwaggerClient.from_url(hostname + '/apispec/ngfw.json', http_client=http_client, config={'validate_responses':False})
    return client

# ----------------
def create_url_object(client):
    url_object = client.get_model("URLObject")(type="urlobject")
    url_object.name = "DNEbadguys"
    #Mission TODO: Enter the domain you found malicious or questionable in Umbrella Investigate to block on FTD
    url_object.url = ""
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
    message = spark.messages.create(SPARK_ROOM_ID,
    text='MISSION: 0day FDM Blocking the Domain URL - I have completed the mission!')
    #Mission TODO3: Print the response
    print(message)

if __name__ == '__main__':
    login()
    client = get_spec_json()
    create_url_object(client)
    create_access_rule(client)
