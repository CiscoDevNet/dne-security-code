import requests
import json
import sys

api_key = ''

#TODO: Enter from the example given in the learning lab
SHA256 = '3b0fa8068f11dc9abf3a4017920ec16303f99999e7276678f19c6b4eecf65287'

#TODO: Enter from the example given in the learning lab
url ='https://panacea.threatgrid.com/api/v2/search/submissions?q={}&api_key={}'.format(SHA256,api_key)
try:
    r = requests.get(url) #TODO enter the right GET method call on requests. Please refer to other code files in this repo
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
