import requests
import json
import sys
#TODO: Enter the key provided by the DNE instructor or your own threatgrid api key
api_key = ''
#TODO: Enter the resource URL
url =''.format(api_key)
try:
	r = requests.get(url)
	status_code = r.status_code
	resp = r.text	
	if (status_code == 200):
		json_resp = json.loads(resp)
		
		resp2=json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': '))
		print(resp2)
		#TODO: Create a file save the token into a text file, Hint refer to the python example on previous page in lab
			
	else:
		r.raise_for_status()
		print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err)) 
finally:
    if r : r.close()
