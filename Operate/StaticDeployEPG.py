#!/usr/bin/env python3

""" Summary:  Logs into ACI APIC and statically deploys an EPG. 

    Description: 
        This will statically deploy an EPG on the ports defined in the 
        yml file. This is useful if you have non-VMM integrated servers
        and multiple EPGs to statically deploy on ACI leaf ports.

        IN DEVELOPMENT (Note: code template based off createVLANPool.py)
        
    Requirements: 
        apicLogin.py
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.0"
__email__ = "brumer@cisco.com"
__status__ = "Development"


# Import built-in modules
import requests, json, time, os, sys
# Import third-party modules
import argparse
# import getpass


# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    # The below import module(s) were placed in the main function for backward compatibility
    from apicLogin import aaaLogin
    
    # Statically specify the APIC URL, if not executing script via CLI
    DefaultApicUrl = 'sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = '!v3G@!4@Y'

    ymlfilename = r'\vepgs.csv'

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
    #### CREATE ME!!###
    json_object = buildJSON(args)

    # Get the authorization cookie from the APIC
    cookies = aaaLogin(DefaultApicUrl, login, passwd)

    # Do the work
    deployEPG(base_url, cookies, args, json_object)


def deployEPG(base_url, cookies, args, json_object):
    sys.exit(0)


if __name__ == "__main__":
    main()
