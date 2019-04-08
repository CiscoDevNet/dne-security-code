# SOLUTION SECTION #3 MISSION UMBRELLA LAB 5-HandsOn-Investigate-API-Hunting

# import necessary libraries / modules
import requests
import json
from datetime import datetime

# copy paste INVESTIGATE API key from previous section within the quotes
investigate_api_key = "<insert-investigate-api-key-here>"

# URL needed for the domain status and category (INVESTIGATE API)
investigateUrl = "https://investigate.api.umbrella.com/domains/categorization/"

# copy paste ENFORCEMENT API key from previous section within the quotes
enforcement_api_key = "<insert-enforcement-api-key-here"

# URL needed to do POST requests for ENFORCEMENT API
eventurl = "https://s-platform.api.opendns.com/1.0/events"

# ensemble URL needed for POST request for ENFORCEMENT API
UrlPost = eventurl+'?customerKey='+enforcement_api_key

# domains that will be checked
domains = ["internetbadguys.com", "cnn.com", "cisco.com", "google.com", "news.com.com"]

# put in right format to pass as argument in POST request
values = str(json.dumps(domains))

# time for timestamp of verdict domain
time = datetime.now().isoformat()

#create header for authentication
headers = {
    'Authorization': 'Bearer ' + investigate_api_key
}

# do GET request for the domain status and category
req = requests.post(investigateUrl, data=values, headers=headers)

# create empty list for malicious domains that need to be added to block list
maliciousDomains = []

# error handling if true then the request was HTTP 200, so successful
if(req.status_code == 200):
    #give user feedback
    print("SUCCESS: Investigate POST request has the following code: 200\n")

    # output of request in variable
    output = req.json()

    # loop through domains and retrieve status for domains
    for domain in domains:
        domainOutput = output[domain]
        domainStatus = domainOutput["status"]
        # walk through different options of status
        if(domainStatus == -1):
            print("The domain %(domain)s is found MALICIOUS at %(time)s\n" % {'domain': domain, 'time': time})

            # add domain to list if malicious
            maliciousDomains.append(domain)
        elif(domainStatus == 1):
            print("The domain %(domain)s is found CLEAN at %(time)s\n" % {'domain': domain, 'time': time})
        else:
            print("The domain %(domain)s is found UNDEFINED / RISKY at %(time)s\n" % {'domain': domain, 'time': time})
else:
    print("An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" % {'error': req.status_code})

# create empty list to contain security events that can be uploaded to Umbrella Enforcement API
data = []

# loop through malicious domains, create security events and append to empty data list
for maliciousDomain in maliciousDomains:
    entry = {
        "alertTime": time + "Z",
        "deviceId": "ba6a59f4-e692-4724-ba36-c28132c761de",
        "deviceVersion": "13.7a",
        "dstDomain": domain,
        "dstUrl": "http://" + domain + "/",
        "eventTime": time + "Z",
        "protocolVersion": "1.0a",
        "providerName": "Security Platform"
    }
    data.append(entry)

# POST REQUEST for Enforcement API: post request ensembly
reqEnf = requests.post(UrlPost, data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})

# error handling if true then the request was HTTP 202, so successful
if(reqEnf.status_code == 202):
    print("SUCCESS: Enforcement POST request has the following code: 202\n")
    for maliciousDomain in maliciousDomains:
        print("The following domain: (%(domain)s) was added to your Block List, timestamp: %(time)s\n" % {'domain': maliciousDomain, 'time': time})
else:
    print("An error has ocurred with the following code %(error)s, please consult the following link: https://enforcement-api.readme.io/" % {'error': req.status_code})
