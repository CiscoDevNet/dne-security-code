#!/usr/bin/env python

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

FDM_USER = "apiuser"
FDM_PASSWORD = "C1sc0123"
FDM_HOST = "10.19.66.126"
FDM_PORT = "40003"

   
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
    payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(username, password)
    
    request = requests.post("https://{}:{}/api/fdm/v1/fdm/token".format(host, FDM_PORT),
                          data=payload, verify=False, headers=headers)
    if request.status_code == 400:
        raise Exception("Error logging in: {}".format(request.content))
    try:
        access_token = request.json()['access_token']
    except:
        raise
        
    return access_token
    
if __name__ == "__main__":

    token = fdm_login()
    print(token)