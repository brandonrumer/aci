#!/usr/local/bin/python3

""" Summary: Creates ACI tenant

    Requirements: 
        apicLogin.py
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.2"
__email__ = "brumer@cisco.com"
__status__ = "Production"


import requests, json, pprint, time, argparse
# import getpass


# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def createtenant(base_url, cookies, new_tenant):
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

    api_url = "/api/mo/uni.json"
    full_url = base_url + api_url
    response_data = requests.post(full_url, cookies=cookies, data=json_object, verify=False)

    # Validate tenant was created
    if response_data.ok:
        # Wait for tenant to be added all the way
        time.sleep(3)
        print(f'Tenant {new_tenant} created. Validating...')
        tenant_url = base_url + f"/api/mo/uni/tn-{new_tenant}.json"
        tenantstatus = requests.get(tenant_url, cookies=cookies, verify=False)
        if tenantstatus.ok:
            data = tenantstatus.json()
            #print(data)
            modTs = data["imdata"][0]['fvTenant']['attributes']['modTs']
            print(f"Tenant {new_tenant} created/modified at {modTs} GMT")
    else:
        # The initial HTTP POST failed; print details
        print(f"Device addition failed with code {response_data.status_code}")
        print(f"Failure body: {response_data.text}")


def main():
    # The below import module(s) were placed in the main function for backward compatibility
    from apicLogin import aaaLogin
    
    # Statically specify the APIC URL, if not executing script via CLI
    DefaultApicUrl = 'sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'
    new_tenant = '20201113-01'
    #login = input('Enter username to connect with: ')
    #passwd = getpass.getpass("Enter password: ")

    # Use argparse to capture any CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--tenant', '-t', action='store', 
        help="The tenant to be created.")
    args = parser.parse_args()
    if args.tenant is not None:
        new_tenant = args.tenant

    base_url = f"https://{DefaultApicUrl}"

    # Get the authorization cookie from the APIC
    cookies = aaaLogin(DefaultApicUrl, login, passwd)

    # Create the tenant
    response_data = createtenant(base_url, cookies, new_tenant)


if __name__ == "__main__":
    main()
