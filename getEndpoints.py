#!/usr/local/bin/python3

""" Summary: Gathers all ACI LLDP info
"""

import requests, json, pprint
from prettytable import PrettyTable
from apicLogin import aaaLogin

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


apicUrl = 'sandboxapicdc.cisco.com'
base_url = f"https://{apicUrl}"

def getendpoints(cookies):
    request_url = '/api/node/class/fvCEp.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify=False)
    endpoint_data = json.loads(response_data.text)
    return endpoint_data

if __name__ == "__main__":
    # Get the login token
    cookies = aaaLogin()

    # Get the endpoints
    endpoint_data = getendpoints(cookies)
    pprint.pprint(endpoint_data)
    quit()

    # Cleanup the endpoint info
    fields = ['mac', 'ip', 'dn']
    data = []

    for endpoint in endpoint_data['imdata']:
        for stuff in endpoint['fvCEp'].items():
            line_dict = {}
            for field in fields:
                line_dict[field] = stuff[1][field]
            data.append(line_dict)

    # pprint.pprint(data)

    table = PrettyTable()
    table.field_names = ['IP Address','MAC Address']
    for row in data:
        table.add_row([row['ip'],row['mac']])
    print(table)


