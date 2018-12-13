#!/usr/bin/env python

import json
import sys
import requests
#Surpress HTTPS insecure errors for cleaner output
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

FMC_USER = "apiuser"
FMC_PASSWORD = "C1sco12345"
FMC_HOST = "198.18.133.9"
FMC_PORT = "443"

def get_auth_token(host=FMC_HOST, username=FMC_USER, password=FMC_PASSWORD):
	""" 
	Authenticates with FMC and returns a token to be used in subsequent API calls
	"""
	headers = {'Content-Type': 'application/json'}
	login_url = "https://{0}:{1}/api/fmc_platform/v1/auth/generatetoken".format(host,FMC_PORT)

	result = requests.post(url=login_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
	result.raise_for_status()
	auth_headers = result.headers
	token = auth_headers.get('X-auth-access-token', default=None)
	uuid = auth_headers.get('DOMAIN_UUID', default=None)
	headers['X-auth-access-token'] = token

	return headers,uuid
	
if __name__ == "__main__":

    headers,uuid = get_auth_token()
    print("Successfully authenticated to FMC\nReceived Auth Token: {0}\nDomain ID: {1}".format(headers['X-auth-access-token'],uuid))
