#!/usr/local/bin/python3

""" Summary:  Master file for b ACI project. 


Requirements: 
    acicobra, pyyaml
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.0"
__email__ = "brumer@cisco.com"
__status__ = "Development"


# Import built-in modules
import os 
import sys
import argparse
import json
import requests

# Import third-party modules
import getpass
import cobra.mit.access
import cobra.mit.session
from prettytable import PrettyTable

# for getEPGs module
from tabulate import tabulate 
from operator import itemgetter 

# Import ACI Modules
from Login.apicLogin import aaaLogin


# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def process_args():
    parser = argparse.ArgumentParser(description='Perform various tasks on a Cisco ACI fabric.', \
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-q',
        '--query', 
        action='store', 
        metavar='query', 
        required=False, 
        help='What to query. Values can be:\n'
        'tenant, epg, bd, endpoints, leaf, lldp_info'
        )
    parser.add_argument(
        '-c',
        '--create', 
        action='store', 
        metavar='create', 
        required=False, 
        help='What to create. Values can be:\n'
        ''
        )
    parser.add_argument(
        '-t',
        '--target', 
        action='store', 
        metavar='target', 
        required=True, 
        help='ACI Fabric IP or hostname.'
        )
    #args = parser.parse_args()
    return parser.parse_args()


def create(cookies, base_url, args, login, passwd):
    print('create')
    print('not yet supported')


def query(cookies, base_url, args, login, passwd):
    print(f'Querying for : {args.query}')
    if args.query.lower() == 'tenant':
        from Query.getTenants import gettenants, cleanupTenants
        tenants_data = gettenants(cookies, base_url)
        table = cleanupTenants(tenants_data)
        print(table)
        print('\n')        
    elif args.query.lower() == 'lldp_info':
        from Query.getLLDP import getlldp, cleanuplldp
        lldp_data = getlldp(cookies, base_url)
        table = cleanuplldp(lldp_data)
        print(table)
        print('\n')        
    elif args.query.lower() == 'endpoints':
        from Query.getEndpoints import getendpoints, cleanendpoints
        endpoint_data = getendpoints(base_url, cookies)
        clean_endpoint = cleanendpoints(endpoint_data)
        print(clean_endpoint)
        print('\n')
    elif args.query.lower() == 'epg':
        # This module uses the CobraSDK, so it has to be called a bit different
        from Query.cobra_getEPGs import getEPG, cleanupEPG
        # Log into the APIC using CobraSDK
        moDir = getCobraLogin(base_url, login, passwd)
        # Get the EPGs
        fvAEPg_objlist = getEPG(moDir)
        # Cleanup the EPGs to alphabetical 
        sortedEPGList = cleanupEPG(fvAEPg_objlist)
        print(tabulate(sortedEPGList, tablefmt="grid", headers="keys"))
        # Log out of the APIC
        moDir.logout()
        print('\n')        

    else:
        print('Query object not found. Quitting')
        sys.exit(0)


def getCobraLogin(base_url, login, passwd):
    # Login to the APIC using CobraSDK
    DefaultApicUrl = base_url.replace('https://', '')
    from Query.cobra_apicLogin import apicLogin 
    moDir=apicLogin(DefaultApicUrl, login, passwd)
    return moDir


def main():
    args = process_args()
    apicUrl = args.target
    base_url = f"https://{apicUrl}"

    ### Coment/uncomment the below static entries if using getpass ###
    login = 'admin'
    passwd = 'ciscopsdt'
    #login = input('Enter username to connect with: ')
    #passwd = getpass.getpass("Enter password: ")
        
    cookies = aaaLogin(apicUrl, login, passwd)

    print('\n')

    # login and passwd are used for Cobra modules. Clean this up later
    if args.query is not None:
        query(cookies, base_url, args, login, passwd)
    else:
        print('Action argument invalid. Quitting...')
        sys.exit(1)        

    '''
    except Exception:
        print('Ran into an exception. Quitting...')
        sys.exit(1)
    '''


if __name__ == "__main__":
    main()

