# SOLUTION SECTION #2 GET REQUEST THREAT GRID LAB 5-HandsOn-Investigate-API-Hunting

# import necessary libraries / modules
import requests
import json
from datetime import datetime

# copy paste API key from previous section within the quotes
APIkey = "<insert-investigate-api-key-here>"

# URL needed for the domain status and category
investigateUrl = "https://investigate.api.umbrella.com/samples/"

# domain that will be checked
domain = "internetbadguys.com"

#create header for authentication and set limit of sample return to 1
headers = {
  'Authorization': 'Bearer ' + APIkey,
  'limit': '1'
}

# assemble the URI, show labels give readable output
getUrl = investigateUrl + domain

# do GET request for the domain status and category
req = requests.get(getUrl, headers=headers)

# time for timestamp of verdict domain
time = datetime.now().isoformat() 

# error handling if true then the request was HTTP 200, so successful
if(req.status_code == 200):
	# store json output in variable
	output = req.json()
	# check if there are associated samples for domain
	if(output["samples"] == []):
		print("No associated samples for %(domain)s at %(time)s" % {'domain': domain, 'time': time})
	else:
		# go through json and store hash and score in variable
		sample = output["samples"][0]
		hashSample = sample["sha256"]
		scoreSample = sample["threatScore"]

		# print hash and score of domain
		print("SUCCESS: The domain %(domain)s has an associated sample with Hash: %(hash)s and Threat Score: %(score)i at %(time)s" % {'domain': domain, 'hash': hashSample, 'score': scoreSample, 'time': time})
else:
	# error handling
	print("An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" % {'error': req.status_code})
