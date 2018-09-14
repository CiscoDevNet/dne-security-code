import requests
import json
# Disable SSL Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
#BONOS TODO: You can create the function definitions to do GET and POST operations

#main code TODO: ENTER YOU CLIENT ID AND API KEY HERE
client_id = "1512e5b0c0c2f2b85401"
api_key = "eaef340f-0ccd-46a5-bcd3-dd62dcbdfb02"

sha_256="3372c1edab46837f1e973164fa2d726c5c6f17dcb888828ccd7c4dfcc234a375"

#TODO: Create the URL /v1/file_lists/simple_custom_detections is the api endpoint.

file_list_url = "https://{}:{}@amp.dcloud.cisco.com/v1/file_lists/simple_custom_detections".format(client_id,api_key)

#First do the GET request to find the custom blacklist file exists
response = requests.get(file_list_url, verify=False)
print(file_list_url)
file_lists= response.json()
#TODO: Parse the response json, and find the "File Blacklist" 
print(file_lists)
for item in file_lists["data"]:
	if item["name"] == "File Blacklist":
		list_id = item["guid"]

print(list_id)
#Create the payload to update the list with new SHA
post_this =  {'description':'created by DNE user using API'}
#TODO: Create the POST URL and Add sha to it
add_list_url = "https://{}:{}@amp.dcloud.cisco.com/v1/file_lists/{}/files/{}".format(client_id, api_key,list_id, sha_256)
print(add_list_url)
print(json.dumps(post_this))
#TODO: Now you have URL figured out, Do your POST to update the SHA in the blacklist.
response = requests.post(add_list_url, post_this, verify=False)
#add_item = post(add_list_url, json.dumps(post_this))

print(response)
