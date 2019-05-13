#!/usr/bin/env python
"""Verify the AMP for Endpoints APIs are accessible and responding.

Verify that DNA Center Sanbox Northbound APIs are accessible and
responding with data.


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

import sys
from pathlib import Path

import requests
from crayons import blue, green, red
from requests import HTTPError
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))

import env_lab  # noqa
import env_user 

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_amp_events(
    host=env_lab.AMP.get("host"),
    client_id=env_user.AMP_CLIENT_ID,
    api_key=env_user.AMP_API_KEY,
):
    """Get a list of recent events from Cisco AMP."""
    print("\n==> Getting recent events from AMP")

    url = f"https://{client_id}:{api_key}@{host}/v1/events"

    response = requests.get(url, verify=False)
    response.raise_for_status()

    events_list = response.json()

    print(green(f"Retrieved events from AMP..."))

    return events_list


def verify() -> bool:
    """Verify access to the AMP for Endpoints APIs."""
    print(blue('\n\n==> Verifying access to the AMP for Endpoints APIs'))
     # Verify the Spark Room exists and is accessible via the access token
    try:
        if(len(get_amp_events())):
            print(green(f"AMP for endpoints API is accessible!\n"))
        else:
            print(red(f"AMP for endpoints API is accessible, API credentials might be wrong"))
    except:
        print(red("Unable to contact AMP for Endpoints"))
        return False
   
    return True


if __name__ == '__main__':
    verify()
