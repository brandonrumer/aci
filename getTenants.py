#!/usr/local/bin/python3

""" Summary: Gathers all ACI LLDP info
"""

import requests, json, pprint
from apicLogin import aaaLogin
from prettytable import PrettyTable

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


apicUrl = 'sandboxapicdc.cisco.com'
base_url = f"https://{apicUrl}"

def gettenants(cookies):
    request_url = '/api/node/class/fvTenant.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify=False)
    tenants_data = json.loads(response_data.text)
    return tenants_data


if __name__ == "__main__":
    cookies = aaaLogin()
    tenants_data = gettenants(cookies)
    
    #pprint.pprint(tenants)

    # Cleanup the endpoint info
    fields = ['name']
    data = []

    for tenant in tenants_data['imdata']:
        for stuff in tenant['fvTenant'].items():
            line_dict = {}
            for field in fields:
                line_dict[field] = stuff[1][field]
            data.append(line_dict)

    # pprint.pprint(data)

    table = PrettyTable()
    table.field_names = ['Tenant Name']
    for row in data:
        table.add_row([row['name']])
    print(table)

