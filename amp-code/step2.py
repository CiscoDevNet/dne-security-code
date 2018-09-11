import requests
import json

#function definitions
def get(url):
	try:
	    response = requests.get(url)
	    # Consider any status other than 2xx an error
	    if not response.status_code // 100 == 2:
	        return "Error: Unexpected response {}".format(response)
	    try:
	        return response.json()
	    except:
	        return "Error: Non JSON response {}".format(response.text)
	except requests.exceptions.RequestException as e:
	    # A serious problem happened, like an SSLError or InvalidURL
	    return "Error: {}".format(e)

#main code TODO: ENTER YOU CLIENT ID AND API KEY HERE
client_id = ""
api_key = ""


event_id_url = "https://{}:{}@api.amp.cisco.com/v1/event_types".format(client_id,api_key)

event_ids= get(event_id_url)

print event_ids
