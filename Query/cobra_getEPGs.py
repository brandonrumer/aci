#!/usr/local/bin/python3

""" Summary: Gathers all EPGs and displays their AP and Tenant

Requirements: 
    acicobra, acimodel, tabulate
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.1"
__email__ = "brumer@cisco.com"
__status__ = "Production"


# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import cobra.mit.access
import cobra.mit.session
from tabulate import tabulate

# For sorting the final result
from operator import itemgetter 


def getEPG(modir):
    class_query = cobra.mit.access.ClassQuery('fvAEPg')
    fvAEPg_objlist = modir.query(class_query)
    return fvAEPg_objlist


def cleanupEPG(fvAEPg_objlist):    
    EPGList = []
    for mo in fvAEPg_objlist:
        # Find the mo's objects, via https://{apic}/visore.html
        dn = str(mo.dn)

        # Break up the dn
        broken_dn = dn.split('/')

        # Get the tenant
        fv_tenant = broken_dn[1]
        tenant = fv_tenant.replace('tn-', '')

        # Get the Application
        ap_application = broken_dn[2]
        application = ap_application.replace('ap-', '')

        row = {
            "EPG": mo.name,
            "AP": application,
            "Tenant": tenant
        }
        EPGList.append(row)
    
    # Sort the list by the Tenant, then App, then EPG. Need to use itemgetter
    #   because the list contains dicts
    sortedEPGList = sorted(EPGList, key=itemgetter("Tenant", "AP", "EPG"))
    
    return sortedEPGList


def main():
    # The below import module(s) were placed in the main function for backward compatibility
    from cobra_apicLogin import apicLogin 

    # Statically specify the APIC URL, if not executing script via CLI
    DefaultApicUrl = 'sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'

    #login = input('Enter username to connect with: ')
    #passwd = getpass.getpass("Enter password: ")
    

    # Login to the APIC using CobraSDK
    moDir=apicLogin(DefaultApicUrl, login, passwd)

    # Get the EPGs
    fvAEPg_objlist = getEPG(moDir)

    # Cleanup the EPGs to alphabetical 
    sortedEPGList = cleanupEPG(fvAEPg_objlist)
    print(tabulate(sortedEPGList, tablefmt="grid", headers="keys"))

    # Cleanup
    moDir.logout()


if __name__ == "__main__":
    main()
