# SOLUTION SECTION #2 GET REQUEST LAB 5-HandsOn-Investigate-API-Hunting

# import necessary libraries / modules
import requests
import json
from datetime import datetime

# copy paste API key from previous section within the quotes
APIkey = "<insert-investigate-api-key-here>"

# URL needed for the domain status and category
investigateUrl = "https://investigate.api.umbrella.com/domains/categorization/"

# domain that will be checked
domain = "internetbadguys.com"

#create header for authentication
headers = {
  'Authorization': 'Bearer ' + APIkey
}

# assemble the URI, show labels give readable output
getUrl = investigateUrl + domain + "?showLabels"

# do GET request for the domain status and category
req = requests.get(getUrl, headers=headers)

# time for timestamp of verdict domain
time = datetime.now().isoformat() 

# error handling if true then the request was HTTP 200, so successful
if(req.status_code == 200):
	# retrieve status for domain
	output = req.json()
	domainOutput = output[domain]
	domainStatus = domainOutput["status"]
	# walk through different options of status
	if(domainStatus == -1):
		print("SUCCESS: The domain %(domain)s is found MALICIOUS at %(time)s" % {'domain': domain, 'time': time})
	elif(domainStatus == 1):
		print("SUCCESS: The domain %(domain)s is found CLEAN at %(time)s" % {'domain': domain, 'time': time})
	else:
		print("SUCCESS: The domain %(domain)s is found UNDEFINED / RISKY at %(time)s" % {'domain': domain, 'time': time})
else:
	print("An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" % {'error': req.status_code})
