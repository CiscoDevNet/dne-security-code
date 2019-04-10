#!/usr/bin/env python
"""Configure FMC Access Policies and Rules.

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

from crayons import blue, green


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / "..").resolve()

sys.path.insert(0, str(repository_root))
sys.path.insert(0, str(here))

from fmc_requests import fmc_authenticate, fmc_post  # noqa


# Authenticate with FMC
print(blue("===> Authenticating to FMC"))
fmc_authenticate()


# Configure an Access Policy
print(blue("\n===> Configuring Access Policy"))
access_policy = {
    "type": "AccessPolicy",
    "name": "DNE Security Access Control Policy",
    "description": "Basic AC Policy",
    "defaultAction": {"action": "BLOCK"},
}

created_policy = fmc_post("policy/accesspolicies", access_policy)

print(f"""
{green("Policy Created:")}
{pformat(access_policy)}
""")


# Configure an Access Rule
print(blue("\n===> Configuring Access Rule"))
access_rule = {
    "action": "ALLOW",
    "enabled": True,
    "type": "AccessRule",
    "name": "Rule1",
    "sourceNetworks": {
        "objects": [
            {
                "type": "Network",
                "overridable": False,
                "id": "005056B8-1C9D-0ed3-0000-085899345923",
                "name": "DNE_Security_Internal_Network",
            }
        ]
    },
    "sendEventsToFMC": False,
    "logFiles": False,
    "logBegin": False,
    "logEnd": False,
}

created_rule = fmc_post(
    endpoint_path=f"policy/accesspolicies/{created_policy['id']}/accessrules",
    data=access_rule,
)

print(f"""
{green("Access Rule Created:")}
{pformat(created_rule)}
""")
