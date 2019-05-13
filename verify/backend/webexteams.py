#!/usr/bin/env python
"""Verify the Webex Teams APIs are accessible and responding.

Verify that user's provide SPARK_ACCESS_TOKEN is valid and that calls to the
Webex Teams APIs complete successfully.


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
import json
import sys
from pathlib import Path

import requests
import webexteamssdk
from crayons import blue, green, red
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))

import env_lab  # noqa
import env_user  # noqa


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def verify() -> bool:
    """Verify access to the Webex Teams APIs."""
    print(blue("\n==> Verifying access to the Webex Teams APIs"))

    # Check to ensure the user has provided their Spark Access Token
    if not env_user.WEBEX_TEAMS_ACCESS_TOKEN:
        print(
           red( "\nFAILED: You must provide your WEBEX_TEAMS_ACCESS_TOKEN in the "
            "env_user.py file.\n")
        )
        return False
    try:
        teams = webexteamssdk.WebexTeamsAPI(env_user.WEBEX_TEAMS_ACCESS_TOKEN)
        me = teams.people.me()
    except webexteamssdk.ApiError as e:
        print(
            red(f"\nFAILED: The API call to Webex Teams returned the following "
            "error:\n{e}\n"))
        return False
    else:
        print(
            green(f"\nYou are connected to Webex Teams as: {me.emails[0]}\n")
        )
    

    # Check to ensure the user has provided a WebEx TEAMS Room ID
    if not env_user.WEBEX_TEAMS_ROOM_ID:
        print(
            red("\nFAILED: You must provide the WEBEX_TEAMS_ROOM_ID of the room you "
            "want to work with in the env_user.py file.\n")
        )
        return False

    # Verify the Spark Room exists and is accessible via the access token
    try:
        room = teams.rooms.get(env_user.WEBEX_TEAMS_ROOM_ID)
    except webexteamssdk.ApiError as e:
        print(
            red(f"\nFAILED: There was an error accessing the Spark Room using the WEBEX_TEAMS_ROOM_ID you provided; error details:\n{e}\n"))
        return False
    else:
        print(
            green(f"You will be posting messages to the following room: {room.title}\n"))

    return True


if __name__ == '__main__':
    verify()
