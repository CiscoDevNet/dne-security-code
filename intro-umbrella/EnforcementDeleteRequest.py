# SOLUTION SECTION #3 DELETE REQUEST LAB 3-HandsOn-Enforcement-API-CustomBlockList

# import necessary libraries / modules
import requests

# copy paste API key from previous section within the quotes
enforcement_api_key = "<insert-enforcement-api-key-here>"

# URL needed to do DELETE (and GET) requests
domain_url = "https://s-platform.api.opendns.com/1.0/domains"

delete_domain = "internetbadguys2.com"

url_delete = domain_url+'?customerKey='+enforcement_api_key+'&where[name]='+delete_domain

req = requests.delete(url_delete)

# error handling if true then the request was HTTP 204, so successful
if(req.status_code == 204):
    print("SUCCESS: the following domain is deleted from your current custom Block List: %(domain)s" %{'domain': delete_domain})
else:
    print("An error has ocurred with the following code %(error)s, please consult the following link: https://enforcement-api.readme.io/" % {'error': req.status_code})
