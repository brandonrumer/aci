#!/usr/local/bin/python3

""" Summary: Gathers all connected endpoints

Requirements: 
    acitoolkit, prettytable
"""

import acitoolkit.acitoolkit as aci
import sys, re
from prettytable import PrettyTable


def apicLogin():
    apicUrl = 'sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'
    base_url = f"https://{apicUrl}"

    session = aci.Session(base_url, login, passwd)
    resp = session.login()

    if not resp.ok:
        print("ERROR: Could not login into APIC: %s" % apicUrl)
        sys.exit(0)
    else:
        print("SUCCESS: Logged into APIC: %s" % apicUrl)
    
    return session


def main():
    apicLogin()

if __name__ == '__main__':
    main()