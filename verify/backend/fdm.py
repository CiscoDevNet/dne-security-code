#!/usr/bin/env python
"""Verify the FDM APIs are accessible and responding.



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

from env_lab import FDM  # noqa


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def fdm_login(
    host=FDM.get("host"),
    port=FDM.get("port"),
    username=FDM.get("username"),
    password=FDM.get("password"),
):
    """Login to FDM and return an access token that may be used for API calls.
    """
    print("\n==> Logging into FDM and requesting an access token")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    response = requests.post(
        f"https://{host}:{port}/api/fdm/v1/fdm/token",
        headers=headers,
        json=payload,
        verify=False,
    )

    try:
        response.raise_for_status()
        access_token = response.json()["access_token"]

    except HTTPError:
        if response.status_code == 400:
            raise HTTPError(f"Error logging in to FDM: {response.text}")
        else:
            raise

    except ValueError:
        raise ValueError("Error parsing the response from FDM")

    return access_token


def verify() -> bool:
    """FDM APIs"""
    print(blue("\n==> Verifying access to the FDM APIs"))
    
    try:
        if(len(fdm_login())):
            print(green(f"Firepower FDM API is accessible...Note: FDM 90 day Eval License needs to enabled for full functionality..!!!\n"))
        else:
            print(red(f"Firepower FDM API is accessible, API credentials might be wrong"))
    except:
        print(red("Unable to contact FDM"))
        return False

    return True


if __name__ == '__main__':
    verify()
