#!/usr/bin/env python
"""Verify the ThreatGrid APIs are accessible and responding.



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

from env_lab import THREATGRID  # noqa
from env_user import THREATGRID_API_KEY  # noqa

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def ThreatGrid_get():
    api_key = THREATGRID_API_KEY
    print("\n==> Getting recent events from ThreatGrid")
    url = 'https://panacea.threatgrid.com/api/v2/iocs/feeds/domains?after=2018-07-18T21:39:13Z&before=2019-07-18T22:39:13Z&domain=lamp.troublerifle.bid&api_key={}'.format(api_key)
    r = requests.get(url)
    r.raise_for_status()
    print(green(f"Retrieved events from ThreatGrid..."))

    return (r.json())


def verify() -> bool:
    """ThreatGrid APIs"""
    print(blue("\n==> Verifying access to the ThreatGrid APIs"))
    
    try:
        if(len(ThreatGrid_get())):
            print(green(f" ThreatGrid API is accessible!\n"))
        else:
            print(red(f" ThreatGrid API is accessible, API credentials might be wrong"))
    except:
        print(red("Unable to contact ThreatGrid Cloud"))
        return False

    return True


if __name__ == '__main__':
    verify()
