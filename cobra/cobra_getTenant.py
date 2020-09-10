#!/usr/local/bin/python3

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
import cobra.mit.access
import cobra.mit.session
from tabulate import tabulate


def connect_to_apic():
    apicUrl = 'https://sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'
    modir = MoDirectory(LoginSession(apicUrl, login, passwd))
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
        #print(mo.name)

        row = {
            "name": mo.name
        }
        TenantList.append(row)

    print(tabulate(TenantList, tablefmt='grid', headers="keys"))

if __name__ == "__main__":
    main()
