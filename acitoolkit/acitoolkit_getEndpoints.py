#!/usr/local/bin/python3

""" Summary: Gathers all ACI LLDP info
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


if __name__ == "__main__":
    session = apicLogin()
    endpoints = aci.Endpoint.get(session)
    # print(endpoints)

    data = []

    for endpoint in endpoints:
        if endpoint.if_dn:
            for dn in endpoint.if_dn:
                match = re.match('protpaths-(\d+)-(\d+)', dn.split('/')[2])
                if match:
                    if match.group(1) and match.group(2):
                        interface = "Nodes: " + match.group(1) + "-" + match.group(2) + " " + endpoint.if_name
        else:
            interface = endpoint.if_name
        '''
        print(f"MAC:{endpoint.mac}")
        print(f"IP:{endpoint.ip}")
        print(f"Interface:{interface}")
        print("--------------------")
        '''
        data_row = {"MAC":endpoint.mac, "IP":endpoint.ip, "Interface":interface}
        data.append(data_row)

    table = PrettyTable()
    table.field_names = ["MAC Address", "IP", "Interface"]
    for row in data:
        table.add_row([row["MAC"],row["IP"],row["Interface"]])
    
    print(table)

    print("\n")
