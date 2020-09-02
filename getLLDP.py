#!/usr/local/bin/python3

""" Summary: Gathers all ACI LLDP info
"""

import requests, json, pprint
from apicLogin import aaaLogin

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


apicUrl = 'sandboxapicdc.cisco.com'
base_url = f"https://{apicUrl}"

def getlldp(cookies):
    request_url = '/api/node/class/lldpAdjEp.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify=False)
    lldp_data = json.loads(response_data.text)
    return lldp_data


if __name__ == "__main__":
    cookies = aaaLogin()
    
    lldp = getlldp(cookies)
    
    pprint.pprint(lldp)

