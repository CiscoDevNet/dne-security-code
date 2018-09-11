# SOLUTION SECTION #3 DELETE REQUEST LAB 3-HandsOn-Enforcement-API-CustomBlockList

# import necessary libraries / modules
import requests

# copy paste API key from previous section within the quotes
custkey = "<insert-enforcement-api-key-here>"

# URL needed to do DELETE (and GET) requests
domainUrl = "https://s-platform.api.opendns.com/1.0/domains"

deleteDomain = "internetbadguys2.com"

UrlDelete = domainUrl+'?customerKey='+custkey+'&where[name]='+deleteDomain

req = requests.delete(UrlDelete)

# error handling if true then the request was HTTP 204, so successful 
if(req.status_code == 204):
    print("SUCCESS: the following domain is deleted from your current custom Block List: %(domain)s" %{'domain': deleteDomain})
else:
    print("An error has ocurred with the following code %(error)s, please consult the following link: https://enforcement-api.readme.io/" % {'error': req.status_code})