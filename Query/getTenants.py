#!/usr/bin/env python3

""" Summary: Gathers all ACI LLDP info
"""

import requests
import json

from prettytable import PrettyTable

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def gettenants(cookies, base_url):
    request_url = '/api/node/class/fvTenant.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify=False)
    tenants_data = json.loads(response_data.text)
    return tenants_data


def cleanupTenants(tenants_data):
    # Cleanup the endpoint info
    fields = ['name']
    data = []

    for tenant in tenants_data['imdata']:
        for stuff in tenant['fvTenant'].items():
            line_dict = {}
            for field in fields:
                line_dict[field] = stuff[1][field]
            data.append(line_dict)

    table = PrettyTable()
    table.field_names = ['Tenant Name']
    for row in data:
        table.add_row([row['name']])
    return(table)


def main():
    # The below import module(s) were placed in the main function for backward compatibility
    from apicLogin import aaaLogin

    apicUrl = 'sandboxapicdc.cisco.com'
    base_url = f"https://{apicUrl}"

    # Coment/uncomment the below static entries if using getpass
    login = 'admin'
    passwd = 'ciscopsdt'
    # login = input('Enter username to connect with: ')
    # passwd = getpass.getpass("Enter password: ")

    cookies = aaaLogin(apicUrl, login, passwd)
    tenants_data = gettenants(cookies, base_url)
    table = cleanupTenants(tenants_data)

    print(table)


if __name__ == "__main__":
    main()
