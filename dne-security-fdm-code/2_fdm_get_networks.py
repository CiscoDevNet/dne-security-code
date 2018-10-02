#!/usr/bin/env python

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

FDM_USER = "admin"
FDM_PASSWORD = "C1sco12345"
FDM_HOST = "198.18.133.8"
FDM_PORT = "443"

   
def fdm_login(host=FDM_HOST,username=FDM_USER,password=FDM_PASSWORD):
    '''
    This is the normal login which will give you a ~30 minute session with no refresh.  
    Should be fine for short lived work.  
    Do not use for sessions that need to last longer than 30 minutes.
    '''
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization":"Bearer"
    }
    payload = {"grant_type": "password", "username": username, "password": password}
    
    request = requests.post("https://{}:{}/api/fdm/v1/fdm/token".format(host, FDM_PORT),
                          json=payload, verify=False, headers=headers)
    if request.status_code == 400:
        raise Exception("Error logging in: {}".format(request.content))
    try:
        access_token = request.json()['access_token']
        return access_token
    except:
        raise

def fdm_get_networks(host,token):
    '''
    This is a GET request to obtain the list of all Network Objects in the system.
    '''
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization":"Bearer {}".format(token)
    }
    try:
        request = requests.get("https://{}:{}/api/fdm/v1/object/networks".format(host, FDM_PORT),
                           verify=False, headers=headers)
        return request.json()
    except:
        raise

if __name__ == "__main__":

    token = fdm_login()
    print(token)
    networks = fdm_get_networks(FDM_HOST,token)
    print(json.dumps(networks,indent=4,sort_keys=True))
