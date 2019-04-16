#!/usr/bin/env python
"""Check for a 'DNE Security Access Control Policy' and remove it if found.

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

from crayons import blue, green


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))
sys.path.insert(0, str(here))


from fmc_requests import fmc_authenticate, fmc_get, fmc_delete  # noqa


# Authenticate with FMC
fmc_authenticate()


# Get the configured access policies
print(blue("\n==> Retrieving the configured access policies"))

configured_policies = fmc_get("policy/accesspolicies")

print(
    green("Successfully retrieved the list of configured access policies"),
    f"Retrieved {len(configured_policies['items'])} policies",
    sep="\n"
)


# Look for a policy named "DNE Security Access Control Policy"
print(blue("\n==> Looking for the 'DNE Security Access Control Policy'"))

for policy in configured_policies["items"]:
    if policy["name"] == "DNE Security Access Control Policy":
        print("Policy found")

        print(blue("\n==> Deleting the `DNE Security Access Control Policy`"))

        fmc_delete(f"policy/accesspolicies/{policy['id']}")

        print(green("Policy deleted"))

        break

else:
    print(green(
        "The `DNE Security Access Control Policy` doesn't exist; "
        "you are good to go!"
    ))
