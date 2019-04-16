#!/usr/bin/env python
"""Helper functions to authenticate with FMC and send basic CRUD requests.

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


import sys
from pathlib import Path

import requests
from crayons import blue, green
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))
sys.path.insert(0, str(here))

from env_lab import FMC  # noqa


# Global Variables
domain_uuid = ""
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Helper Functions
def fmc_authenticate(
    host=FMC.get("host"),
    port=FMC.get("port"),
    username=FMC.get("username"),
    password=FMC.get("password"),
):
    """Authenticate with FMC; get and store the auth token and domain UUID."""
    print(blue("\n==> Authenticating with FMC and requesting an access token"))

    global domain_uuid

    authentication = HTTPBasicAuth(username, password)

    response = requests.post(
        f"https://{host}:{port}/api/fmc_platform/v1/auth/generatetoken",
        headers=headers,
        auth=authentication,
        verify=False
    )
    response.raise_for_status()

    # Get the authentication token and domain UUID from the response
    access_token = response.headers.get("X-auth-access-token")
    domain_uuid = response.headers.get("DOMAIN_UUID")

    # Update the headers used for subsequent requests to FMC
    headers["DOMAIN_UUID"] = domain_uuid
    headers["X-auth-access-token"] = access_token

    print(
        green('Successfully authenticated to FMC!'),
        f"Domain UUID: {domain_uuid}",
        f"Access Token: {access_token}",
        sep="\n"
    )

    return access_token, domain_uuid


def create_url(endpoint_path, host=FMC.get("host"), port=FMC.get("port")):
    """Create an FMC configuration API endpoint URL."""
    return f"https://{host}:{port}/api/fmc_config/v1" \
           f"/domain/{domain_uuid}/{endpoint_path}"


def fmc_post(endpoint_path, data):
    """Send a POST request to FMC and return the parsed JSON response."""
    url = create_url(endpoint_path)

    print("Sending POST request to", url)
    response = requests.post(url, headers=headers, json=data, verify=False)
    response.raise_for_status()

    return response.json()


def fmc_get(endpoint_path):
    """Send a GET request to FMC and return the parsed JSON response."""
    url = create_url(endpoint_path)

    print("Sending GET request to", url)
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()

    return response.json()


def fmc_delete(endpoint_path):
    """Send a DELETE request to FMC and return the parsed JSON response."""
    url = create_url(endpoint_path)

    print("Sending DELETE request to", url)
    response = requests.delete(url, headers=headers, verify=False)
    response.raise_for_status()

    return response.json()


# If this script is the "main" script, run...
if __name__ == "__main__":
    fmc_authenticate()
