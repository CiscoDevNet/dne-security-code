#!/usr/bin/env python
"""Verify the ISE APIs are accessible and responding.

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
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))

from env_lab import ISE  # noqa


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_ise_anc_policies(
    host=ISE.get("host"),
    port=ISE.get("port"),
    username=ISE.get("username"),
    password=ISE.get("password"),
):
    """Get a list of configured ISE Adaptive Network Control (ANC) policies."""
    print("\n==> Getting ISE ANC policies")

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json"
        }

    authentication = HTTPBasicAuth(username, password)

    response = requests.get(
        f"https://{host}:{port}/ers/config/ancpolicy",
        headers=headers,
        auth=authentication,
        verify=False,
    )
    response.raise_for_status()

    return response.json()["SearchResult"]["resources"]

def verify() -> bool:
    """Verify access to the ISE ERS REST APIs."""
    print(blue("\n==> Verifying access to the ISE ERS REST APIs for Environment."))
    try:
        if(len(get_ise_anc_policies())):
            print(green(f"ISE ERS REST API is accessible!\n"))
        else:
            print(red(f"ISE ERS REST API is accessible, API credentials might be wrong"))
    except:
        print(red("Unable to contact ISE ERS REST API"))
        return False

    return True


if __name__ == "__main__":
    verify()
