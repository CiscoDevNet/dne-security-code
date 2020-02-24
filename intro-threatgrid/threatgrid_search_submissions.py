#!/usr/bin/env python
"""Search ThreatGrid Submissions.

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
from crayons import blue, green, red, white


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / "..").resolve()

sys.path.insert(0, str(repository_root))

from env_lab import THREATGRID  # noqa
from env_user import THREATGRID_API_KEY  # noqa


def search_threatgrid_submissions(
    sha256,
    host=THREATGRID.get("host"),
    api_key=THREATGRID_API_KEY,
):
    """Search TreatGrid Submissions, by sha256.

    Args:
        sha256(str): Lookup this hash in ThreatGrid Submissions.
        host(str): The ThreatGrid host.
        api_key(str): Your ThreatGrid API key.
    """
    print(blue(f"\n==> Searching the ThreatGrid Submissions for: {sha256}"))

    query_parameters = {
        "q": sha256,
        "api_key": api_key,
    }
    
    response = requests.get(
        f"https://{host}/api/v2/search/submissions",
        params=query_parameters,
    )
    response.raise_for_status()

    submission_info = response.json()["data"]["items"]

    if submission_info:
        print(green("Successfully retrieved data on the sha256 submission"))
    else:
        print(red("Unable to retrieve data on the sha256 submission"))
        sys.exit(1)

    return submission_info


# If this script is the "main" script, run...
if __name__ == "__main__":
    if len(sys.argv) == 2:
        _, sha256 = sys.argv
    else:
        print(f"{white('Usage:', bold=True)} {Path(__file__).name} SHA256")
        sys.exit(1)
    """ #TODO Call the proper function """
    submission_info = 

    submission_info_path = here / f"{sha256}-submission-info.json"
    print(blue(f"\n==> Saving submission info to: {submission_info_path}"))
    """ #TODO Pass the file path to open function to write the file """
    with open(#TODO:) as file:
        json.dump(submission_info, file, indent=2)
