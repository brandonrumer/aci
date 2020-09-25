#!/usr/local/bin/python3

""" Summary: Gets LLDP info for all connected devices.

"""

__author__ = "Brandon Rumer"
__version__ = "1.0.0"
__email__ = "brumer@cisco.com"
__status__ = "Production"

import requests, json, argparse, pprint
from apicLogin import aaaLogin
# import getpass

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getlldp(cookies, base_url):
    request_url = '/api/node/class/lldpAdjEp.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify=False)
     # If the post fails, raise the HTTPError, otherwise continue
    response_data.raise_for_status() 
    lldp_data = json.loads(response_data.text)
    return lldp_data


def main():
    # Statically specify the APIC URL, if not executing script via CLI
    DefaultApicUrl = 'sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'
        
    #login = input('Enter username to connect with: ')
    #passwd = getpass.getpass("Enter password: ")
    
    # Use arg parse to capture any CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--apic', '-a', action='store', 
        help="The IP or URL of the APIC controller. This should not include \
            http(s) or a trailing backslash.")

    args = parser.parse_args()
    apicUrl = args.apic

    if apicUrl == None:
        apicUrl = DefaultApicUrl
    
    base_url = f"https://{apicUrl}"

    cookies = aaaLogin(apicUrl, login, passwd)
    
    lldp_data = getlldp(cookies, base_url)
    
    pprint.pprint(lldp_data)

if __name__ == "__main__":
    main()