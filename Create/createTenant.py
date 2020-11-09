#!/usr/local/bin/python3

""" Summary: Creates ACI tenant

    Requirements: 
        apicLogin.py
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.1"
__email__ = "brumer@cisco.com"
__status__ = "Production"


import requests, json, pprint, time
#from apicLogin import aaaLogin
#from getTenants import gettenants, cleanupTenants
#from prettytable import PrettyTable

# import getpass

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def createtenant(base_url, cookies, json_object):
    api_url = "/api/mo/uni.json"
    full_url = base_url + api_url
    response_data = requests.post(full_url, cookies=cookies, data=json_object, verify=False)
    #response = json.loads(response_data.text)
    return response_data


def main():
    apicUrl = 'sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'
    new_tenant = "20200903-02"

    #login = input('Enter username to connect with: ')
    #passwd = getpass.getpass("Enter password: ")


    base_url = f"https://{apicUrl}"

    # Begin building the dataset
    data = {
    "fvTenant" : {
        "attributes" : {
        "name" : new_tenant
        }
    }
    }

    # Create the JSON object from the data 
    json_object = json.dumps(data)

    # Get the authorization cookie from the APIC
    cookies = aaaLogin(apicUrl, login, passwd)

    # Create the tenant
    response_data = createtenant(base_url, cookies, json_object)

    # Verify it worked
    if response_data.ok:
        # Wait for tenant to be added all the way
        time.sleep(3)
        print('Tenant created. Validating...')
        tenants_data = gettenants(cookies, base_url)
        table = cleanupTenants(tenants_data)
        print(table)
    else:
        # The initial HTTP POST failed; print details
        print(f"Device addition failed with code {response_data.status_code}")
        print(f"Failure body: {response_data.text}")


if __name__ == "__main__":
    main()
