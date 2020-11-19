#!/usr/bin/env python3

""" Summary:  Logs into ACI APIC and creates a VLAN Pool. 

    Description: 
        The VLAN Pool must be specified in the python code.  
        The file should only have VLAN numbers, each on a 
        different line with no seperator other than a line break.
        
    Requirements: 
        apicLogin.py
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.3"
__email__ = "brumer@cisco.com"
__status__ = "Production"


# Import built-in modules
import requests, json, time, os, sys
# Import third-party modules
import argparse
# import getpass


# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def createVLANPool(base_url, cookies, args, json_object):
    try:
        if args.option:
            try:
                name, pooltype = args.option.split(',')
            except KeyError:
                print('Name and Pool type are invalid. Quitting...')
                sys.exit(0)
    except AttributeError:
        pass
    try:
        if args.pooltype:
            pooltype = args.pooltype
            name = args.name
    except AttributeError:
        pass
    
    api_url = f"/api/node/mo/uni/infra/vlanns-[{name}]-{pooltype}.json"
    full_url = base_url + api_url

    # Post the data
    response_data = requests.post(full_url, cookies=cookies, data=json_object, verify=False)

    # Verify it worked
    if response_data.ok:
        # Wait for tenant to be added all the way
        time.sleep(3)
        print('Pool created.')
    else:
        # The initial HTTP POST failed; print details
        print(f"Device addition failed with code {response_data.status_code}")
        print(f"Failure body: {response_data.text}")


def buildJSON(args):
    # Try block is to allow for standalone runs as well as bACI integration
    try:
        if args.option:
            try:
                name, pooltype = args.option.split(',')
            except KeyError:
                print('Name and Pool type are invalid. Quitting...')
                sys.exit(0)
    except AttributeError:
        pass
    try:
        if args.pooltype:
            pooltype = args.pooltype
            name = args.name
    except AttributeError:
        pass

    vlanlist = []
    try:
        # Open the file and strips blank lines
        with open(args.file, "r") as file_in:
            for line in file_in:
                if not line.isspace():
                    line = line.replace('\n', '')
                    vlanlist.append(line)
    except FileNotFoundError:
        print('CSV VLAN file not found. Quitting...')
        sys.exit(0)

    # Create the JSON child objects (vlan block)
    childrenkey = []
    for vlan in vlanlist:
        childrenkey.append({
                "fvnsEncapBlk":{
                    "attributes":{
                        "dn":f"uni/infra/vlanns-[{name}]-{pooltype}/from-[vlan-{vlan}]-to-[vlan-{vlan}]",
                        "from":f"vlan-{vlan}",
                        "to":f"vlan-{vlan}",
                        "rn":f"from-[vlan-{vlan}]-to-[vlan-{vlan}]"
                    }
                }
        })

    # Put all the JSON together
    data = {
    "fvnsVlanInstP":{
        "attributes":{
            "dn":f"uni/infra/vlanns-[{name}]-{pooltype}",
            "name":name,
            "rn":f"vlanns-[{name}]-{pooltype}"
        },
        "children":childrenkey
    }
    }

    # Create the JSON object from the data 
    json_object = json.dumps(data)
    #print(json_object)
    return json_object


def main():
    # The below import module(s) were placed in the main function for backward compatibility
    from apicLogin import aaaLogin
    
    # Statically specify the APIC URL, if not executing script via CLI
    DefaultApicUrl = 'sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'

    ymlfilename = r'\vlans.csv'
    vlanpoolname = 'TEST_Pool'
    assignmethod = 'dynamic'  # set 'dynamic' or 'static'

    #login = input('Enter username to connect with: ')
    #passwd = getpass.getpass("Enter password: ")

    # Use argparse to capture any CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', '-n', action='store', 
        help="Defines the name if the VLAN pool")    
    parser.add_argument('--pooltype', '-p', action='store', 
        help="Defines if the VLAN Pool Type should be 'static' or 'dynamic' assigned")
    parser.add_argument('--file', '-f', action='store', 
        help="The input file of VLANs. The file should only have VLAN numbers, each on a \
        different line with no seperator other than a line break")
    args = parser.parse_args()

    # Doing some arg magic so this can be ran with bACI.py or standalone
    if args.file == None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        ymlfile=dir_path + ymlfilename
        args.file = ymlfile
    if args.name == None:
        args.name = vlanpoolname
    if args.pooltype == None:
        args.pooltype = assignmethod

    base_url = f"https://{DefaultApicUrl}"
    
    # Build the JSON for the post to APIC
    json_object = buildJSON(args)

    # Get the authorization cookie from the APIC
    cookies = aaaLogin(DefaultApicUrl, login, passwd)

    # Create the pool
    #createVLANPool(DefaultApicUrl, cookies, vlanpoolname, assignmethod, json_object)
    createVLANPool(base_url, cookies, args, json_object)


if __name__ == "__main__":
    main()

