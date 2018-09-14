# SOLUTION SECTION #2 POST REQUEST LAB 5-HandsOn-Investigate-API-Hunting

# import necessary libraries / modules
import requests
import json
from datetime import datetime

# copy paste API key from previous section within the quotes
APIkey = "<insert-investigate-api-key-here>"

# URL needed for the domain status and category
investigateUrl = "https://investigate.api.umbrella.com/domains/categorization/"

# domains that will be checked
domains = ["internetbadguys.com", "cnn.com", "cisco.com"]

# put in right format to pass as argument in POST request
values = str(json.dumps(domains))

#create header for authentication
headers = {
  'Authorization': 'Bearer ' + APIkey
}

# do GET request for the domain status and category
req = requests.post(investigateUrl, data=values, headers=headers)

# time for timestamp of verdict domain
time = datetime.now().isoformat() 

# error handling if true then the request was HTTP 200, so successful
if(req.status_code == 200):
	#give user feedback
	print("SUCCESS: request has the following code: 200\n")

	# output of request in variable
	output = req.json()

	# loop through domains and retrieve status for domains
	for domain in domains:
		domainOutput = output[domain]
		domainStatus = domainOutput["status"]
		# walk through different options of status
		if(domainStatus == -1):
			print("The domain %(domain)s is found MALICIOUS at %(time)s\n" % {'domain': domain, 'time': time})
		elif(domainStatus == 1):
			print("The domain %(domain)s is found CLEAN at %(time)s\n" % {'domain': domain, 'time': time})
		else:
			print("The domain %(domain)s is found UNDEFINED / RISKY at %(time)s\n" % {'domain': domain, 'time': time})
else:
	print("An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" % {'error': req.status_code})
