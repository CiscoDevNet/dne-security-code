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

def post(url,data):
	try:
	    response = requests.post(url, data)
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
sha_256=d15766ead5d8ffe68fd96d4bda75c07378fc74f76e251ae6631f4ec8226d2bcb

file_list_url = "https://{}:{}@api.amp.cisco.com/v1/file_lists/simple_custom_detections".format(client_id,api_key)

file_lists= get(file_list_url)

for item in file_lists["data"]:
	if item["name"] == "File Blacklist":
		list_id = item["guid"]

post_this =  {"description":"created by DNE user using API"}
add_list_url = "https://{}:{}@api.amp.cisco.com/v1/file_lists/{}/files/{}".format(client_id, api_key,list_id, sha_256)

add_item = post(add_list_url, json.dumps(post_this))

print add_item
