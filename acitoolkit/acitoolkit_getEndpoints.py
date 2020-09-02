#!/usr/local/bin/python3

""" Summary: Gathers all ACI LLDP info
"""

import acitoolkit.acitoolkit as aci
import sys

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


if __name__ == "__main__":
    session = apicLogin()
    endpoints = aci.Endpoint.get(session)
    # print(endpoints)

    for endpoint in endpoints:
        print(f"MAC:{endpoint.mac}")
        print(f"IP:{endpoint.ip}")
        print("---------------------")

