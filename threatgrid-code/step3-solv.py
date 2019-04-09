#STEP3
import requests
import json
import sys

api_key = ''

url ='https://panacea.threatgrid.com/api/v2/iocs/feeds/domains?after=2018-07-18T21:39:13Z&before=2019-07-18T22:39:13Z&domain=lamp.troublerifle.bid&api_key={}'.format(api_key)
try:
    r = requests.get(url)
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        json_resp = json.loads(resp)
        resp2=json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': '))
        print(resp2)
        #save the token into a text file
        fh = open("resultat.txt", "w")
        fh.write(resp2)
        fh.close()
    else:
        r.raise_for_status()
        print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err))
finally:
    if r : r.close()
