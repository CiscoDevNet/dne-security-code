#!/usr/bin/env python
"""
Copyright (c) 2018-2019 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from datetime import datetime
import requests
import socket
import configparser
import json
import sys
from pathlib import Path

from crayons import blue, green, red
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." ).resolve()

sys.path.insert(0, str(repository_root))

sys.path.insert(0, str(repository_root))

from env_lab import UMBRELLA  # noqa
from env_user import UMBRELLA_INVESTIGATE_KEY  # noqa
# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# SOLUTION SECTION #2 POST REQUEST LAB 5-HandsOn-Investigate-API-Hunting

# import necessary libraries / modules
import requests
import json
from datetime import datetime

# API key from evn_user.py
investigate_api_key = UMBRELLA_INVESTIGATE_KEY

# URL needed for the domain status and category
# investigate_url = "https://investigate.api.umbrella.com/domains/categorization/"
inv_u = UMBRELLA.get("inv_url")
investigate_url = f"{inv_u}/domains/categorization/" 

# domains that will be checked


# put in right format to pass as argument in POST request


#create header for authentication
headers = {
    'Authorization': 'Bearer ' + investigate_api_key
}

def get_umbrella_dispos(domains):
    # put in right format to pass as argument in POST request
    values = str(json.dumps(domains))
    req = requests.post(investigate_url, data=values, headers=headers)
    # time for timestamp of verdict domain
    time = datetime.now().isoformat()
    # error handling if true then the request was HTTP 200, so successful
    if(req.status_code == 200):
        print("SUCCESS: request has the following code: 200\n")
        output = req.json()
        for domain in domains:
            domain_output = output[domain]
            domain_status = domain_output["status"]
            if(domain_status == -1):
                print("The domain %(domain)s is found MALICIOUS at %(time)s\n" % {'domain': domain, 'time': time})
            elif(domain_status == 1):
                print("The domain %(domain)s is found CLEAN at %(time)s\n" %
                  {'domain': domain, 'time': time})
            else:
                print("The domain %(domain)s is found UNDEFINED / RISKY at %(time)s\n" %
                  {'domain': domain, 'time': time})
    else:
        print("An error has ocurred with the following code %(error)s, please consult the following link: https://docs.umbrella.com/investigate-api/" %
              {'error': req.status_code})

if __name__ == "__main__":
    #TODO Call the function to get dispostion on these domains 
    domains = ["internetbadguys.com", "cnn.com", "cisco.com"]
    get_umbrella_dispos(domains)
