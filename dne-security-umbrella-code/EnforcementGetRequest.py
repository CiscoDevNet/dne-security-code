# SOLUTION SECTION #4 GET REQUEST LAB 3-HandsOn-Enforcement-API-CustomBlockList

# import necessary libraries / modules
import requests
import json

# copy paste API key from previous section within the quotes
custkey = "<insert-enforcement-api-key-here>"

# URL needed to do GET requests
domainUrl = "https://s-platform.api.opendns.com/1.0/domains"

UrlGet = domainUrl+'?customerKey='+custkey

# create empty list to contain all domains already in Umbrella
domainList = []

# keep doing GET requests, until looped through all domains
while True:
    req = requests.get(UrlGet)
    JsonFile = req.json()
    for row in JsonFile["data"]:
        domainList.append(row["name"])
    # GET requests will only list 200 domains, if more than that, it will request next bulk of 200 domains
    if bool(JsonFile["meta"]["next"]):
        Url = JsonFile["meta"]["next"]
    # break out of loop when finished
    else:    
        break

# error handling if true then the request was HTTP 200, so successful 
if(req.status_code == 200):
  print("SUCCESS: the following domain(s) are in your current custom Block List:")
  print(domainList)
else:
  print("An error has ocurred with the following code %(error)s, please consult the following link: https://enforcement-api.readme.io/" % {'error': req.status_code})