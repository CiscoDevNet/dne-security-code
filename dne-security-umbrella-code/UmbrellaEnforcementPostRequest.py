# SOLUTION SECTION #3 POST REQUEST LAB 3-HandsOn-Enforcement-API-CustomBlockList

# import necessary libraries / modules
import requests
from datetime import datetime
import json

# copy paste API key from previous section within the quotes
custkey = "<insert-enforcement-api-key-here>"

# URL needed to do POST requests
eventurl = "https://s-platform.api.opendns.com/1.0/events"

# time for AlertTime and EventTime when domains are added to Umbrella
time = datetime.now().isoformat() 

# domain that will be uploaded
domain = "internetbadguys.com"

# URL needed for POST request
UrlPost = eventurl+'?customerKey='+custkey

# NOTE: Although this information MUST be provided when using the API, not all of it is utilized in the destination lists within Umbrella
data = {
"alertTime": time + "Z",
"deviceId": "ba6a59f4-e692-4724-ba36-c28132c761de",
"deviceVersion": "13.7a",
"dstDomain": domain,
"dstUrl": "http://" + domain + "/",
"eventTime": time + "Z",
"protocolVersion": "1.0a",
"providerName": "Security Platform"
}

# POST REQUEST: post request ensembly
req = requests.post(UrlPost, data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})

# error handling if true then the request was HTTP 202, so successful
if(req.status_code == 202):
  print("SUCCESS: domain (%(domain)s) was accepted, HTTP response: 202, timestamp: %(time)s" % {'domain': domain, 'time': time})
else:
  print("An error has ocurred with the following code %(error)s, please consult the following link: https://enforcement-api.readme.io/" % {'error': req.status_code})
