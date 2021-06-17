## Cisco DevNet DevNet Express Security Track Code

This repository contains the sample code to go along with [Cisco DevNet Learning Labs](https://developer.cisco.com/learning) covering security topics. During the setup steps of the labs, you'll be asked to clone this repository down to your workstation to get started.

## Getting started
1. Go to <https://developer.cisco.com/learning/tracks/devnet-express-security#dne-security-verify> and login or register if you're not registered.
2. Follow the instructions in the lab. The lab environment offers a step-by-step path to configure and run the examples of this repository.

## Technical requirements
You may either do the labs in the virtual environment offered by Cisco or configure your own environment on your desktop.

## Accessing Cisco virtual lab environment
You need a PC or MAC with the following software: 
- Anyconnect VPN client : either the package provided by Cisco for Windows environment or the free client available on Linux platform, openconnect <http://ubuntuhandbook.org/index.php/2014/11/connect-cisco-anyconnect-vpn-ubuntu/>.
- RDP client to connect to windows, either the RDP client embarked in any windows OS or a free alternative such as Remmina <https://remmina.org/how-to-install-remmina/>.
The connection parameters are provided in the lab environment.

## Working on your own desktop
### Python 3.6
Python is required to run the sample scripts.

You have to install Python 3.6. We suggest that you work in a virtual environment to work with Python. If you want to know more about virtual env, this document is an excellent introduction <http://christopher5106.github.io/python/2017/10/12/python-packages-and-their-managers-apt-yum-easy_install-pip-virtualenv-conda.html>. The lab explains how to install virtual-env. You can work with Miniconda as an alternative. To install Miniconda, follow the official instructions here: <https://conda.io/miniconda.html>.

### Postman
You use Postman to test REST API calls in a graphical environment. To install Postman, follow the official instructions here: <https://learning.getpostman.com/docs/postman/launching_postman/installation_and_updates/>.

### Creating virtual env with Conda
You should run the following commands on Linux to create a virtual environment with Conda:
```
$conda create --name cisco python=3.6
$source activate cisco
```
and you're done!

## Contributing
Contributions are welcome, and we are glad to review changes through pull requests. See [contributing.md](contributing.md) for details.

The goal of these learning labs is to ensure a 'hands-on' learning approach rather than just theory or instructions.

## About this Sample Code

Contributions are welcome, and we are glad to review changes through pull requests. See [contributing.md](contributing.md) for details.

Within this repository are several files and folders covering different topics and labs.  This table provides details on what each is used for, and which labs they correspond to.  

| File / Folder                                  | Description                 |
|:-----------------------------------------------|:----------------------------|
| [`env_lab.py`](env_lab.py)                     | A Python file containing lab infrastructure details for routers, switches and appliances leveraged in the different labs.  This file provides a centralized  Python `import` that is used in  other code samples to retrieve IPs, usernames, and passwords for connections |
| [`env_user.template`](env_user.template)       | Similar to `env_lab.py`, this is a template for end users to copy within their own code repo as `env_user.py` where they can provide unique details for their own accounts.  For example, their Webex Teams (formerly Cisco Spark) authentication token.  Not all labs require this file, if one does it will be specified in setup. |
| [`requirements.txt`](requirements.txt)         | Global Python requirements file containing the requirements for **all** labs within this repository.  Each folder also contains a local `requirements.txt` file. |
| [`intro-python-code/`](intro-python-code/)     | Sample code and exercises for the [Python Fundamentals Learning Labs](https://developer.cisco.com/learning/modules/programming-fundamentals/parsing-json-python/step/1) Pulled in through a file copy in November 2018. Note that the submodule tracks with the `master` branch, but solutions are on the `solution` branch in the [original CiscoDevNet/intro-python-code repository](https://github.com/CiscoDevNet/intro-python-code). <br> |
| [`intro-rest-api/`](intro-rest-api/)           | Sample code and exercises for the [REST API Fundamentals Learning Labs](https://developer.cisco.com/learning/modules/rest-api-fundamentals/hands-on-postman/step/1) Pulled in through a file copy in November 2018. |
| [`intro-umbrella/`](intro-umbrella/)           | Sample code and exercises for the [Introduction to Cisco Umbrella Learning Labs]() <br> (_Publishing Soon_) |
| [`verify/`](verify/)                           | A series of verification scripts primarily used during DevNet Express events to ensure the workshop environment is fully operational. |
| [`dev/`](dev/)                                 | Resources and information for building code samples and labs. |
| [`requirements-dev.txt`](requirements-dev.txt) | Python requirements file containing requirements only needed if developing new code samples. |

> Note: These code samples are also leveraged during DevNet Express events.  If you are one of these events, your event proctors and hosts will walk you through event setup and verification steps as part of agenda.  

> Note: the [`mission-data`](https://github.com/CiscoDevNet/dne-security-code/tree/master/mission-data) directory contains the answsers in JSON files. This is as last resort only when the attendee is not able to solve it. Make sure that the attendees don't use this to "cheat".

## Contributing

These learning modules are for public consumption, so you must ensure that you have the rights to any content that you contribute.

## Getting Involved

* If you’re a Cisco employee and would like to have access to make changes yourself, please add your GitHub ID and we’ll get in touch.
* If you'd like to contribute to an existing lab, refer to [contributing.md](contributing.md).
* If you're interested in creating a new Cisco DevNet Learning Lab, please contact a DevNet administrator for guidance.
