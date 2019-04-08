"""0day Workflow Mission - edit this file
This is your starting point for the 0day workflow  Mission.
Edit this file to
 - 
There are a few places to edit (search for MISSION comments)

Script Dependencies:
    requests
Depencency Installation:
    $ pip install requests
Copyright (c) 2018, Cisco Systems, Inc. All rights reserved.
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
import requests
import json


class tg_account (object):
    """Class to define the threatgrid instance.

    Attributes
    key: API key

    """

    def __init__(self, key):
        """Return Threatgrid Object whose attributes are key."""
        self.key = key
        self.url = "panacea.threatgrid.com/api/v2"
        self.headers = {
            'Content-Type': 'application/json'
            }

    def get(self, path):
        """GET method for Threatgrid."""
        try:
            response = requests.get(
                "https://{}{}&api_key={}".format(self.url, path, self.key),
                headers=self.headers
            )
            # Consider any status other than 2xx an error
            if not response.status_code // 100 == 2:
                return "Error: Unexpected response {}".format(response)
            try:
                return response.json()
            except:
                return "Error: Non JSON response {}".format(response.text)
        except requests.exceptions.RequestException as e:
                # A serious problem happened, like an SSLError or InvalidURL
                return "Error: {}".format(e)
