#!/usr/bin/env python
"""One-line summary of your script.

Multi-line description of your script (make sure you include the copyright and
license notice).


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

import webexteamssdk
from crayons import green


# Get the absolute path for the directory where this file is located
here = Path(__file__).parent.absolute()

# Get the path for the project / repository root
repository_root = (here / "..").resolve()


# Extend the system path to include the project root and import the env files
sys.path.insert(0, str(repository_root))
import env_lab  # noqa
import env_user  # noqa


# TODO: Insert your code here.  What follows is just an example.


teams = webexteamssdk.WebexTeamsAPI(env_user.WEBEX_TEAMS_ACCESS_TOKEN)


print(f"""
{green("My FMC Lab Environment:")}
    FMC Host: {env_lab.FMC["host"]}
    FMC Port: {env_lab.FMC["port"]}
    FMC Username: {env_lab.FMC["username"]}
    FMC Password: {env_lab.FMC["password"]}
""")


print(f"""
{green("I am connected to Webex Teams as:")}
{teams.people.me()}
""")

print(f"""
{green("I am posting things to the following Teams Room:")}
{teams.rooms.get(env_user.WEBEX_TEAMS_ROOM_ID)}
""")
