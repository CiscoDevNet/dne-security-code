#!/usr/bin/env python
"""Get the list of all networks in FDM.

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
from pprint import pformat

import requests
from crayons import blue, green, white
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))
sys.path.insert(0, str(here))

from env_lab import FDM  # noqa
from fdm_auth import fdm_login  # noqa


# Data for the network object to be created
NETWORK_OBJECT = {
    "name": "PUT_NAME_HERE",
    "description": "DevNet Security",
    "subType": "HOST",
    "value": "5.5.5.5",
    "type": "networkobject"
}


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def fdm_create_network(
    network_object,
    access_token,
    host=FDM.get("host"),
    port=FDM.get("port"),
    api_version=FDM.get("api_version"),
):
    """Create a new network in FDM."""
    print(blue("\n==> Creating a new network in FDM"))

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    payload = network_object

    response = requests.post(
        f"https://{host}:{port}/api/fdm/v{api_version}/object/networks",
        headers=headers,
        json=payload,
        verify=False,
    )
    response.raise_for_status()

    print(green("Successfully created the new network!"))
    return response.json()


# If this script is the "main" script, run...
if __name__ == "__main__":
    token = fdm_login()
    new_network_details = fdm_create_network(NETWORK_OBJECT, token)

    print(
        white("Network Details:", bold=True),
        pformat(new_network_details),
        sep="\n"
    )
