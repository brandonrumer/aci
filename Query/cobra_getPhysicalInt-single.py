#!/usr/bin/env python3

""" Summary: Gets physical interfaces of a single ACI Nexus switch

Requirements: 
    acicobra, acimodel

"""

__author__ = "Brandon Rumer"
__version__ = "0.0.1"
__email__ = "brumer@cisco.com"
__status__ = "Development"


import cobra.mit.access
import cobra.mit.naming
import cobra.mit.request
import cobra.mit.session
import cobra.model.infra
from cobra.internal.codec.xmlcodec import toXMLStr
import re

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def connect_to_apic():
  """ APIC Login """
  apicUrl = 'https://sandboxapicdc.cisco.com'
  login = 'admin'
  passwd = 'ciscopsdt'
  ls = cobra.mit.session.LoginSession(apicUrl, login, passwd)
  md = cobra.mit.access.MoDirectory(ls)
  md.login()
  return md


def getIfName(intf):
    """ Gets the interface name. Cobra returns physical interface
        name as: phys-[eth1/98] """
    name = None
    idx = None

    match = re.search('\[(eth\d+/\d+)\]', str(intf.dn))
    if match:
        name = match.group(1)
        match = re.search('(\d+)/(\d+)', name)
        if match:
            idx = 200*int(match.group(1)) + int(match.group(2))

    return name, idx 


def getPhysInt(md):
    """ Gets the physical interface """
    #api/mo/topology/pod-1/node-1/sys
    intfs = md.lookupByClass("l1PhysIf", parentDn=dn) 
    pmifs = md.lookupByClass("ethpmPhysIf", parentDn=dn)
            

    # l1PhysIf has the name of interface and admin status
    # ethpmPhysIf has the operation status
    #dn = str("uni/infra/accportprof-Leaf101") + '/sys'
    intfs = md.lookupByClass("l1PhysIf", parentDn=dn) 
    pmifs = md.lookupByClass("ethpmPhysIf", parentDn=dn)
    print(intfs, pmifs)
            
    iftable = {}
    for intf in intfs:
        name, idx = getIfName(intf)
        if name and idx:
            iftable[idx] = [name, intf.adminSt, "Unknown"]
    for intf in pmifs:
        name, idx = getIfName(intf)
        if name and idx:
            list = iftable[idx]
            list[2] = intf.operSt
            iftable[idx] = list

    # print the interface status
    interfaces = []
    for idx, list in sorted(iftable.items()):
        interfaces.append(list[0])
        #print(list[0], list[1], list[2])
            
    print(interfaces)
    return interfaces


def main():
    md = connect_to_apic()
    interfaces = getPhysInt(md)

    md.logout()


if __name__ == "__main__":
    main()
