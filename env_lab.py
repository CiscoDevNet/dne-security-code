"""Set the Environment Information Needed to Access Your Lab!

The provided sample code in this repository will reference this file to get the
information needed to connect to your lab backend.  You provide this info here
once and the scripts in this repository will access it as needed by the lab.


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


# User Input

# Please select the lab environment that you will be using today
#     sandbox - Cisco DevNet Always-On / Reserved Sandboxes
#     express - Cisco DevNet Express Lab Backend
#     custom  - Your Own "Custom" Lab Backend
ENVIRONMENT_IN_USE = "express"

# End User Input


# Set the 'Environment Variables' based on the lab environment in use
if ENVIRONMENT_IN_USE == "sandbox":
    # Values for the Reservable FMC Sandbox
    FMC = {
        "host": "fmcrestapisandbox.cisco.com",
        "port": 443,
        "username": "",     # Generated when reserved
        "password": "",     # Generated when reserved
    }

elif ENVIRONMENT_IN_USE == "express":
    # Values for the FMC in the DevNet Express Security dCloud Pod
    FMC = {
        "host": "198.18.133.9",
        "port": 443,
        "username": "apiuser",
        "password": "C1sco12345",
    }
    # Values for the FDM in the DevNet Express Security dCloud Pod
    FDM = {
        "host": "198.18.133.8",
        "port": 443,
        "username": "admin",
        "password": "C1sco12345",
    }
    # Values for the ISE in the DevNet Express Security dCloud Pod
    ISE = {
        "host": "198.18.133.27",
        "port": 9060,
        "username": "ersadmin",
        "password": "C1sco12345",
    }
    # Values for the Umbrella Enforcement API in the DevNet Express Security Session
    ENFORCEMENT = {
        "apiKey" : "PUT THE UMBRELLA ENFORCEMENT KEY HERE"
    }
    # Values for the Umbrella Investigate API in the DevNet Express Security Session
    INVESTIGATE = {
        "token" : "PUT THE UMBRELLA INVESTIGATE KEY HERE" 
    }
    # Values for the AMP for endpoints API in the DevNet Express Security dCloud Pod
    AMP = {
        "clientId" : "PUT THE AMP CLIENT ID HERE",
        "apiKey" : "PUT THE AMP API KEY HERE",
        "host" : "amp.dcloud.cisco.com",
    }
    # Values for the ThreatGrid  in the DevNet Express Security Session
    THREATGRID = {
        "apiKey" : "PUT YOUR THREATGRID API KEY HERE" ,
        "host" : "panacea.threatgrid.com/api/v2",
    }
    # Values for the WebEx Teams in the DevNet Express Security
    WEBEXTEAMS = {
        "apiKey" : "PUT YOUR WEBEX TEAMS API KEY HERE",
        "roomID" : "PUT YOUR WEBEX TEAMS ROOM ID HERE",
    }

elif ENVIRONMENT_IN_USE == "custom":
    # Values for your FMC
    FMC = {
        "host": "",
        "port": 443,
        "username": "",
        "password": "",
    }
