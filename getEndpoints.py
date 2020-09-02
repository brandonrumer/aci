#!/usr/local/bin/python3

""" Summary: Gathers all ACI LLDP info
"""

import requests, json, pprint
from apicLogin import aaaLogin

apicUrl = 'sandboxapicdc.cisco.com'
base_url = f"https://{apicUrl}"

def getendpoints(cookies):
    request_url = '/api/node/class/fvCEp.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify=False)
    endpoint_data = json.loads(response_data.text)
    return endpoint_data


if __name__ == "__main__":
    cookies = aaaLogin()
    
    endpoints = getendpoints(cookies)
    
    pprint.pprint(endpoints)

