#!/usr/local/bin/python3

""" Summary:  Logs into ACI APIC via cobraSDK and creates the several
              Filters in the common tenant. The filters that are crated
              are the commonly used 'literal values and port numbers' 
              that are commonly used inside IOS/XE ACLs.
              
              Code was partially generated via arya.

              getpass can be implemented in cases where this is the sole 
              script that is ran in the environment.

Requirements: 
    acicobra, acimodel
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.0"
__email__ = "brumer@cisco.com"
__status__ = "Development"


import cobra.mit.access
import cobra.mit.naming
import cobra.mit.request
import cobra.mit.session
import cobra.model.infra
from cobra.internal.codec.xmlcodec import toXMLStr

# import getpass

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def connect_to_apic():
  # APIC Login
  apicUrl = 'https://sandboxapicdc.cisco.com'
  login = 'admin'
  passwd = 'ciscopsdt'
  #login = input('Enter username to connect with: ')
  #passwd = getpass.getpass("Enter password: ")
  ls = cobra.mit.session.LoginSession(apicUrl, login, passwd)
  md = cobra.mit.access.MoDirectory(ls)
  md.login()
  return md

def addDefaultFilters(md):
  # Initialize empty dictionary
  '''
  filterkeys = ['filtername', 'vzentryname', 'annotation', 'dFromPort', 'dToPort', 'descr', 'etherT', 'prot', 'sFromPort', 'sToPort', 'stateful']
  filterdict = {}
  for keys in filterkeys:
    filterdict[keys] = ""
  print(filterdict)
  '''

  filters = []
  cmd_FLT = {'filtername':'domain', 
                    'vzentryName':'53-tcp',
                    'annotation':'',
                    'dFromPort':'514',
                    'dToPort':'514',
                    'descr':'',                    
                    'etherT':'ip',
                    'prot':'tcp',
                    'sFromPort':'',
                    'sToPort':'',
                    'stateful':'yes'
  }

  filters.append(cmd_FLT)

  # Top level object on which operations will be made
  topDn = cobra.mit.naming.Dn.fromString('uni/tn-common/flt-cmd')
  topParentDn = topDn.getParent()
  topMo = md.lookupByDn(topParentDn)

  for entry in filters:
    vzFilter = cobra.model.vz.Filter(topMo, name=entry['filtername'])
    vzEntry = cobra.model.vz.Entry(vzFilter, name=entry['vzentryName'], etherT=entry['etherT'], prot=entry['prot'], dFromPort=entry['dFromPort'], dToPort=entry['dFromPort'])
    # Commit
    print("This is the XML to be posted to the APIC:\n")
    print(toXMLStr(topMo))
    c = cobra.mit.request.ConfigRequest()
    c.addMo(topMo)
    md.commit(c)


def main():
  md = connect_to_apic()
  addDefaultFilters(md)
  
  md.logout()


if __name__ == "__main__":
    main()
