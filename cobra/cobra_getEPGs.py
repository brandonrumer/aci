#!/usr/local/bin/python3

""" Summary: Gathers all EPGs and displays their AP and Tenant

Requirements: 
    acicobra, acimodel, tabulate
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.0"
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


def connect_to_apic():
    apicUrl = 'https://sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'
    modir = cobra.mit.access.MoDirectory(cobra.mit.session.LoginSession(apicUrl, login, passwd))
    modir.login()
    return modir


def getEPG(modir):
    class_query = cobra.mit.access.ClassQuery('fvAEPg')
    fvAEPg_objlist = modir.query(class_query)
    return fvAEPg_objlist


def main():
    modir = connect_to_apic()
    fvAEPg_objlist = getEPG(modir)

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

    print(tabulate(sortedEPGList, tablefmt="grid", headers="keys"))

    # Cleanup
    modir.logout()


if __name__ == "__main__":
    main()
