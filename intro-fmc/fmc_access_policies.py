#!/usr/bin/env python
"""Configure FMC Access Policies and Rules.

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
from pprint import pprint


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = os.path.abspath(os.path.dirname(__file__))
repository_root = os.path.abspath(os.path.join(here, ".."))
sys.path.insert(0, repository_root)
sys.path.insert(0, here)

from fmc_requests import fmc_authenticate, fmc_post     # noqa


# Authenticate with FMC
fmc_authenticate()


# Configure an Access Policy
access_policy = {
    "type": "AccessPolicy",
    "name": "DNE Security Access Control Policy",
    "description": "Basic AC Policy",
    "defaultAction": {
        "action": "BLOCK",
    },
}

created_policy = fmc_post("policy/accesspolicies", access_policy)

# Pretty Print the Results
print("")
print("Policy Created:")
pprint(access_policy)
print("")

# Configure an Access Rule

# Inputs
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
                "name": "DNE_Security_Internal_Network"
            }
        ]
    },
    "sendEventsToFMC": False,
    "logFiles": False,
    "logBegin": False,
    "logEnd": False,
}

created_rule = fmc_post(
    endpoint_path="policy/accesspolicies/{policy_id}/accessrules"
                  "".format(policy_id=created_policy["id"]),
    data=access_rule,
)

# Pretty Print the Results
print("")
print("Access Rule Created:")
pprint(created_rule)
print("")
