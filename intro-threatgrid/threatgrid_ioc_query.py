#!/usr/bin/env python
"""Query the ThreatGrid Indication of Compromise (IoC) feed.

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


import json
import sys
from pathlib import Path

import requests
from crayons import blue, green


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / "..").resolve()

sys.path.insert(0, str(repository_root))

from env_lab import THREATGRID  # noqa
from env_user import THREATGRID_API_KEY  # noqa


def query_threatgrid_ioc_feed(
    domain,
    after=None,
    before=None,
    host=THREATGRID.get("host"),
    api_key=THREATGRID_API_KEY,
):
    """Query the IoC feed by domain and return the list of malware samples.

    Args:
        domain(str): Lookup this domain name in the ThreatGrid IoC feed.
        after(str): Query for events that occurred after this datetime.
        before(str): Query for events that occurred before this datetime.
        host(str): The ThreatGrid host.
        api_key(str): Your ThreatGrid API key.
    """
    print(blue(f"\n==> Querying the ThreatGrid IoC feed for domain: {domain}"))

    query_parameters = {
        "domain": domain,
        "after": after,
        "before": before,
        "api_key": api_key,
    }

    response = requests.get(
        f"https://{host}/api/v2/iocs/feeds/domains",
        params=query_parameters,
    )
    response.raise_for_status()

    samples = response.json()["data"]["items"]

    print(green(f"Successfully retrieved data on "
                f"{len(samples)} malware samples"))

    return samples


# If this script is the "main" script, run...
if __name__ == "__main__":
    domain = "lamp.troublerifle.bid"

    malware_samples = query_threatgrid_ioc_feed(
        domain,
        after="2018-07-18T21:39:13Z",
        before="2019-07-18T22:39:13Z",
    )

    malware_samples_path = here / f"{domain}-malware-samples-data.json"
    print(blue(f"\n==> Saving samples data to: {malware_samples_path}"))
    with open(malware_samples_path, "w") as file:
        json.dump(malware_samples, file, indent=2)
