#!/usr/local/bin/python3

""" Summary: Gets physical interface status of ACI Nexus switches

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


# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def main():
    # log into an APIC and create a directory object
    ls = cobra.mit.session.LoginSession('https://sandboxapicdc.cisco.com', 'admin', 'ciscopsdt')
    md = cobra.mit.access.MoDirectory(ls)
    md.login()



if __name__ == "__main__":
    main()
