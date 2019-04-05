import os
import sys
import time
import requests
import requests.auth
from urllib3.exceptions import InsecureRequestWarning
# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = os.path.abspath(os.path.dirname(__file__))
repository_root = os.path.abspath(os.path.join(here, ".."))
sys.path.insert(0, repository_root)
sys.path.insert(0, here)

print ("Reading env.py....")
syms = ['◐', '◓', '◑', '◒']
time.sleep(4)

print ("\nDone Reading... Preparing to Print your config ...")

from env_lab import FMC     #
from env_lab import FDM
from env_lab import ISE
from env_lab import ENFORCEMENT
from env_lab import INVESTIGATE
from env_lab import AMP
from env_lab import THREATGRID
time.sleep(2)
host=FMC["host"]
port=FMC["port"]
username=FMC["username"]
password=FMC["password"]
print("\n\nYour FMC Configuration:\n")
print (f"FMC HOST: {host}") 
print (f"FMC PORT:  {port}")
print (f"FMC UserName: {username}")
print (f"FMC Password: {password}")
host=FDM["host"]
port=FDM["port"]
username=FDM["username"]
password=FDM["password"]
time.sleep(2)
print("\n\nYour FDM Configuration:\n")
print (f"FDM HOST: {host}") 
print (f"FDM PORT:  {port}")
print (f"FDM UserName: {username}")
print (f"FDM Password: {password}")
host=ISE["host"]
port=ISE["port"]
username=ISE["username"]
password=ISE["password"]
time.sleep(2)
print("\n\nYour ISE Configuration:\n")
print (f"ISE HOST: {host}") 
print (f"ISE PORT:  {port}")
print (f"ISE UserName: {username}")
print (f"ISE Password: {password}")
time.sleep(2)
print("\n\nYour Umbrella Configuration:\n")
apikey=ENFORCEMENT["apiKey"]
print (f"Umbrella enforcement Key: {apikey}") 
token=INVESTIGATE["token"]
print (f"Umbrella Investigate Key: {token}") 
custid = AMP["clientId"]
apikey = AMP["apiKey"]
host   = AMP["host"]
time.sleep(2)
print("\n\nYour AMP Configuration:\n")
print (f"AMP Customer ID: {custid}")
print (f"AMP API Key: {apikey}") 
print (f"AMP HOSTNAME: {host}")
time.sleep(2)
print("\n\nYour THREATGRID Configuration:\n")
host = THREATGRID["host"]
apikey = THREATGRID["apiKey"]
print (f"THREATGRID HOST: {host}")
print (f"THREATGRID API KEY: {apikey}\n\n")