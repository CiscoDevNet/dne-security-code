#!/usr/bin/env python
"""Verify the Umbrella Investigate APIs are accessible and responding.



Copyright (c) 2019-2020 Cisco and/or its affiliates.

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
import requests
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
repository_root = (here / ".." / ".." ).resolve()

sys.path.insert(0, str(repository_root))

sys.path.insert(0, str(repository_root))

from env_lab import UMBRELLA  # noqa
from env_user import UMBRELLA_INVESTIGATE_KEY  # noqa
# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# API key from evn_user.py

def doUmbrellaGet() :
    investigate_api_key = UMBRELLA_INVESTIGATE_KEY
    # URL needed for the domain status and category
    #create header for authentication
    headers = {
        'Authorization': 'Bearer ' + investigate_api_key
    }
    # # investigate_url = "https://investigate.api.umbrella.com/domains/categorization/"
    inv_u = UMBRELLA.get("inv_url")
    investigate_url = f"{inv_u}/domains/categorization/" 
    # domain that will be checked
    domain = "internetbadguys.com"
    #create header for authentication
    headers = {
        'Authorization': 'Bearer ' + investigate_api_key
        }
    # assemble the URI, show labels give readable output
    get_url = investigate_url + domain + "?showLabels"

    #do GET request for the domain status and category
    try:
        req = requests.get(get_url, headers=headers)
        
        # time for timestamp of verdict domain
        if(req.status_code == 200):
            return "Green"
        elif(req.status_code == 401):
            return "Yellow"
        else:
            return "Orange"
    except:
        return "Red"


def verify() -> bool:
    print(blue("\n==> Verifying access to the Umbrella Investigate APIs"))

    """ Verify the umbrella investigate accessible via the provided token """
    
    result = doUmbrellaGet()

    if (result == "Green"):
        print(green(f"Umbrella Investigate is accessible and token is good!\n"))
        return True
    elif (result == "Yellow"):
        print(red(f"Umbrella Investigate is accessible But token is NO good!\n"))
        return False
    elif (result == "Orange"):
        print(red(f"Umbrella Investigate is accessible But something went very wrong!\n"))
        return False
    else:
        print(red("Unable to access Umbrella Investigate Cloud\n"))
        return False



if __name__ == '__main__':
    verify()
