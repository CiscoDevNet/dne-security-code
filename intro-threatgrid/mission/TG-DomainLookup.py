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
import json
import threatgrid
from datetime import datetime
import sys
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

#Mission TODO1: Please add your SPARK_ACCESS_TOKEN and SPARK_ROOM_ID here
SPARK_ACCESS_TOKEN = ""
SPARK_ROOM_ID=""

spark = ciscosparkapi.CiscoSparkAPI(SPARK_ACCESS_TOKEN)
# Mission TODO: Insert the SHA you want to hunt using TG


sha_256 = ""

# Mission TODO: enter the api credentials for the TG API access

api_key = ""

# intialize  threatgrid objects

threatgrid_api = threatgrid.tg_account(api_key)

# step one query threatgrid for the sha_256 and extract relevant information
# important info is sample id
# import info is threat_score

samples = threatgrid_api.get("/search/submissions?q={}".format(sha_256))
# dictionary of the samples with their scores and behaviors

#print(json.dumps(samples, indent=4, sort_keys=True))
sample_ids = {}
behaviors = []
for sample in samples['data']['items']:
    sample_ids[sample["item"]["sample"]] = sample["item"]["analysis"]["threat_score"]
    for behavior in sample["item"]["analysis"]["behaviors"]:
        behaviors.append(behavior["title"])

# Prepare TG report to screen with average score after number of runs and behavior
behaviors = set(behaviors)

num_of_runs = len(sample_ids)
total = 0
sample_string = ""
for sample, score in sample_ids.items():
    total = total + score
    sample_string = "{}{},".format(sample_string,sample)
average = total/num_of_runs

print ("Sample was run {} times and results in an average score of {}".format (num_of_runs, average))
print ("Behavior of sample:")
for value in behaviors:
    print (value)
sample_string = sample_string[:-1]
#print sample_string
# now that we got everything from TG lets take the samples and seach them for all domains
domains = threatgrid_api.get("/samples/feeds/domains?sample={}&after=2017-2-2".format(sample_string))
#build a list of domains for Umbrella
domain_list = []
ip_list = []
for domain in domains["data"]["items"]:
    if domain["relation"] == "dns-lookup":
        for item in domain["data"]["answers"]:
            domain_list.append(domain["domain"])
            ip_list.append(item)

message = spark.messages.create(SPARK_ROOM_ID,
    text='MISSION: 0day ThreatGrid - I have completed the mission!')
#Mission TODO3: Print the domains and ip....
print ("\nAssociated domains:\n")
print ("\n".join(domain_list))
print ("\n samples made outbound connections on following IPs:\n")
print ("\n".join(ip_list))
print ("Finished Building list for Next Mission with Umbrella Investigate ...")
