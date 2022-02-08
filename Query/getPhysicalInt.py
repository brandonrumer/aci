#!/usr/bin/env python3

""" Summary: Gets physical interface list of Nexus switches in the ACI fabric

Requirements:
    prettytable

"""

__author__ = "Brandon Rumer"
__version__ = "1.0.1"
__email__ = "brumer@cisco.com"
__status__ = "Production"


import requests
import json
import re
import operator
import argparse
from prettytable import PrettyTable

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getInt(cookies, base_url):
    request_url = '/api/node/class/l1PhysIf.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify=False)
    endpoint_data = json.loads(response_data.text)
    return endpoint_data


def cleanupendpoints(endpoint_data):
    # Cleanup the endpoint info
    fields = ['dn', 'id', 'adminSt', 'status']
    data = []
    for endpoint in endpoint_data['imdata']:
        for stuff in endpoint['l1PhysIf'].items():
            line_dict = {}
            for field in fields:
                line_dict[field] = stuff[1][field]
            data.append(line_dict)

    table = PrettyTable()
    table.field_names = ['Node', 'dn', 'Port', 'adminSt', 'status']
    for row in data:
        try:
            node = re.search(r'node-\d\d\d', str(row["dn"])).group(0)
        except AttributeError:
            node = ''
        table.add_row([node, row['dn'], row['id'], row['adminSt'], row['status']])
    return(table)


def main():
    # The below import module(s) were placed in the main function for backward compatibility
    from apicLogin import aaaLogin

    # Statically specify the APIC URL, if not executing script via CLI
    DefaultApicUrl = 'sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'
    # login = input('Enter username to connect with: ')
    # passwd = getpass.getpass("Enter password: ")

    # Use arg parse to capture any CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--apic',
        '-a',
        action='store',
        help="The IP or URL of the APIC controller. This should not include \
            http(s) or a trailing backslash."
    )

    args = parser.parse_args()
    apicUrl = args.apic

    if apicUrl is None:
        apicUrl = DefaultApicUrl

    base_url = f"https://{apicUrl}"

    cookies = aaaLogin(apicUrl, login, passwd)

    endpoint_data = getInt(cookies, base_url)

    # Cleanup the data
    table = cleanupendpoints(endpoint_data)
    print(table.get_string(sort_key=operator.itemgetter(1, 0), sortby="Node"))


if __name__ == "__main__":
    main()
