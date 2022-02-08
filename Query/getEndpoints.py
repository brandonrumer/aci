#!/usr/bin/env python3

""" Summary: Gathers all ACI LLDP info

    Requirements:
        apicLogin.py, PrettyTable
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.1"
__email__ = "brumer@cisco.com"
__status__ = "Production"

import requests
import json
import argparse
from prettytable import PrettyTable
# import getpass

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getendpoints(base_url, cookies):
    request_url = '/api/node/class/fvCEp.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify=False)
    # If the post fails, raise the HTTPError, otherwise continue
    response_data.raise_for_status()
    endpoint_data = json.loads(response_data.text)
    return endpoint_data


def cleanendpoints(endpoint_data):
    fields = ['mac', 'ip', 'dn']
    data = []

    for endpoint in endpoint_data['imdata']:
        for stuff in endpoint['fvCEp'].items():
            line_dict = {}
            for field in fields:
                line_dict[field] = stuff[1][field]
            data.append(line_dict)

    table = PrettyTable()
    table.field_names = ['IP Address', 'MAC Address']
    for row in data:
        table.add_row([row['ip'], row['mac']])
    return table


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

    # Get the login token
    cookies = aaaLogin(apicUrl, login, passwd)

    # Get the endpoints
    endpoint_data = getendpoints(base_url, cookies)

    # Cleanup the endpoint info
    clean_endpoint = cleanendpoints(endpoint_data)
    print(clean_endpoint)


if __name__ == "__main__":
    main()
