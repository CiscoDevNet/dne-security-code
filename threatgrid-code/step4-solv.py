import requests
import json
import sys

api_key = ''

url ='https://panacea.threatgrid.com/api/v2/search/submissions?q=SHA256&api_key={}'.format(api_key)
try:
	r = requests.get(url)
	#print (r.json())
	status_code = r.status_code
	resp = r.text	
	if (status_code == 200):
        # print("GET successful. Response data --> ")
		json_resp = json.loads(resp)
		#print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
		resp2=json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': '))
		print(resp2)
		#save the token into a text file
		fh = open("resultat-step4.txt", "w")
		fh.write(resp2)
		fh.close() 		
	else:
		r.raise_for_status()
		print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err)) 
finally:
    if r : r.close()