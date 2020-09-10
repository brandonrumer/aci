#!/usr/local/bin/python3

""" Summary: Gathers all the physical inventory

Requirements: 
    acicobra, acimodel, tabulate
"""


# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import cobra.mit.access
import cobra.mit.session
from tabulate import tabulate


def connect_to_apic():
    apicUrl = 'https://sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'
    modir = cobra.mit.access.MoDirectory(cobra.mit.session.LoginSession(apicUrl, login, passwd))
    modir.login()
    return modir


def getTenant(modir):
    class_query = cobra.mit.access.ClassQuery('fvTenant')
    fvTenant_objlist = modir.query(class_query)
    return fvTenant_objlist


def main():
    modir = connect_to_apic()
    fvTenant_objlist = getTenant(modir)

    TenantList = []

    for mo in fvTenant_objlist:
        # Find the mo's objects, via https://{apic}/visore.html
        row = {
            "name": mo.name
        }
        TenantList.append(row)

    print(tabulate(TenantList, tablefmt='grid', headers="keys"))

    # Cleanup
    modir.logout()


if __name__ == "__main__":
    main()
