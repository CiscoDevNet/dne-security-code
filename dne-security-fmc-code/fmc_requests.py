#!/usr/bin/env python
"""Helper functions to authenticate with FMC and send basic CRUD requests.

Copyright (c) 2018 Cisco and/or its affiliates.

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

import os
import sys

import requests
import requests.auth
from urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = os.path.abspath(os.path.dirname(__file__))
repository_root = os.path.abspath(os.path.join(here, ".."))
sys.path.insert(0, repository_root)
sys.path.insert(0, here)

from env_lab import FMC     # noqa


# Constants
FMC_LOGIN_URL = "https://{host}:{port}/api/fmc_platform/v1/auth/generatetoken"
FMC_CONFIG_URL = "https://{host}:{port}/api/fmc_config/v1/" \
                 "domain/{domain_uuid}/{endpoint_path}"


# Global Variables
headers = {"Content-Type": "application/json"}
auth_token = ""
domain_uuid = ""


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Helper Functions
def fmc_authenticate():
    """Authenticate with FMC; get and store the auth token and domain UUID."""
    global auth_token
    global domain_uuid

    login_url = FMC_LOGIN_URL.format(host=FMC["host"], port=FMC["port"])
    authentication = requests.auth.HTTPBasicAuth(
        username=FMC["username"],
        password=FMC["password"],
    )

    try:
        response = requests.post(
            url=login_url,
            headers=headers,
            auth=authentication,
            verify=False,
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as error:
        print("Request Exception:", error)
        sys.exit(1)

    # Get our authentication token and domain UUID from the response
    auth_token = response.headers.get("X-auth-access-token")
    domain_uuid = response.headers.get("DOMAIN_UUID")

    # Update the headers used for requests to FMC
    headers["X-auth-access-token"] = auth_token
    headers["DOMAIN_UUID"] = domain_uuid

    print(
        """
        Successfully authenticated to FMC: {host}
        Received Auth Token: {auth_token}
        For Domain (UUID): {domain_uuid}
        """.format(
            host=FMC["host"],
            auth_token=auth_token,
            domain_uuid=domain_uuid,
        )
    )

    return auth_token, domain_uuid


def create_url(endpoint_path):
    """Create an FMC configuration API endpoint URL."""
    url = FMC_CONFIG_URL.format(
        host=FMC["host"],
        port=FMC["port"],
        domain_uuid=domain_uuid,
        endpoint_path=endpoint_path,
    )

    print("Created URL:", url)

    return url


def fmc_post(endpoint_path, data):
    """Send a POST request to FMC and return the parsed JSON response."""
    url = create_url(endpoint_path)

    try:
        print("Sending POST request to", url)
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()

    except requests.exceptions.RequestException as error:
        print("Request Exception:", error)
        sys.exit(1)

    print("Post was successful, status code:", response.status_code)
    return response.json()


def fmc_get(endpoint_path):
    """Send a GET request to FMC and return the parsed JSON response."""
    url = create_url(endpoint_path)

    try:
        print("Sending GET request to", url)
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()

    except requests.exceptions.RequestException as error:
        print("Request Exception:", error)
        sys.exit(1)

    print("Get was successful, status code:", response.status_code)
    return response.json()


def fmc_delete(endpoint_path):
    """Send a DELETE request to FMC and return the parsed JSON response."""
    url = create_url(endpoint_path)

    try:
        print("Sending DELETE request to", url)
        response = requests.delete(url, headers=headers, verify=False)
        response.raise_for_status()

    except requests.exceptions.RequestException as error:
        print("Request Exception:", error)
        sys.exit(1)

    print("Delete was successful, status code:", response.status_code)
    return response.json()


# If this script is the "main" script running
if __name__ == "__main__":
    fmc_authenticate()
