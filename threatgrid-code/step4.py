#TODO: Enter the API Key provided by DNE instructor or use your own threatgrid api key
api_key = ''
#TODO: Enter the request URL, Hint please refer to the intro-threat-grid-api learning lab
url =''.format(api_key)
try:
	r = requests. #TODO enter the right GET method call on requests. Please refer to other code files in this repo
	#print (r.json())
	status_code = r.status_code
	resp = r.text	
	if (status_code == 200):
		json_resp = json.loads(resp)
		resp2=json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': '))
		print(resp2)
		#save the token into a text file
		fh = open("resultat-step4.txt", "w")
		#TODO Now enter the step to write the contents in the file.. 
		fh.close() 		
	else:
		r.raise_for_status()
		print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err)) 
finally:
    if r : r.close()
