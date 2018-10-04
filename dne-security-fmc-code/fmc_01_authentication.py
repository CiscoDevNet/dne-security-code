#!/usr/bin/env python
"""Authenticate with FMC.

The `get_auth_token_and_domain_uuid()` function authenticates against FMC and
returns the authentication token and domain UUID to be used in subsequent API
requests.
"""

import requests
import requests.auth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Get the absolute path for the directory where this file is located "here"
# Extend the system path to include this directory
here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)

from fmc_environment import FMC_HOST, FMC_PORT, FMC_USER, FMC_PASSWORD


# Constants
FMC_LOGIN_URL = "https://{host}:{port}/api/fmc_platform/v1/auth/generatetoken"


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Helper Functions
def get_auth_token_and_domain_uuid(username=FMC_USER, password=FMC_PASSWORD,
                                   host=FMC_HOST, port=FMC_PORT):
    """Authenticate with FMC; get the auth token and domain UUID."""
    login_url = FMC_LOGIN_URL.format(hostname=host, port=port)
    headers = {"Content-Type": "application/json"}
    authentication = requests.auth.HTTPBasicAuth(username, password)

    response = requests.post(
        url=login_url,
        headers=headers,
        auth=authentication,
        verify=False,
    )
    response.raise_for_status()

    auth_token = response.headers.get("X-auth-access-token")
    domain_uuid = response.headers.get("DOMAIN_UUID")

    print(
        """
        Successfully authenticated to FMC: {host}
        Received Auth Token: {auth_token}
        For Domain (UUID): {domain_uuid}
        """.format(
            host=host,
            auth_token=auth_token,
            domain_uuid=domain_uuid,
        )
    )

    return auth_token, domain_uuid


# If this script is the "main" script running
if __name__ == "__main__":
    get_auth_token_and_domain_uuid()
