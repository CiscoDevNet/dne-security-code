import requests

# retrieve text file with sans domains and write to .txt file
result = requests.get("https://isc.sans.edu/feeds/suspiciousdomains_High.txt")
open('domains.txt', 'wb').write(result.content)

# loop through .txt file and append every domain to list, skip comments
domainList = []
with open('domains.txt') as inputfile:
    for line in inputfile:
        if line[0] == "#" or line.strip() == "Site":
            pass
        else:
            domainList.append(line.strip())

# loop through all domains
for domain in domainList:
    print(domain)

    # DO Umbrella Investigate check

    # if(associated sample has a Threat Score of higher or equal then 90)
        # POST request to Enforcement API
