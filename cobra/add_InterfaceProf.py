#!/usr/local/bin/python3

""" Summary:  Logs into ACI APIC via cobraSDK and creates the Interface 
              Profile interface selectors for every interface on the switch.
               Code was partially generated via arya. 


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


def connect_to_apic():
  # APIC Login
  apicUrl = 'https://sandboxapicdc.cisco.com'
  login = 'admin'
  passwd = 'ciscopsdt'
  ls = cobra.mit.session.LoginSession(apicUrl, login, passwd)
  md = cobra.mit.access.MoDirectory(ls)
  md.login()
  return md


def addIntProf(md):
  # Top level object on which operations will be made
  topDn = cobra.mit.naming.Dn.fromString('uni/infra/accportprof-Leaf101')   #<-- Actual Switch to tie it to
  topParentDn = topDn.getParent()
  topMo = md.lookupByDn(topParentDn)

  # Begin building the request using cobra syntax
  infraAccPortP = cobra.model.infra.AccPortP(topMo, name='Leaf101')   #<--Switch Profile Name

  # Pre-load the first interface because it doesn't actually have a number in the infraHPortS variable (just easier)
  infraHPortS = cobra.model.infra.HPortS(infraAccPortP, type='range', name='1:01')
  infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, fromPort='1', toPort='1', name='block2')
  infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS)

  # Create the rest of the interfaces, using a leading 0 for single digits
  for i in (range(2,48)):
    i2 = ('%02d' % i)
    print(f'i:{i}, i2:{i2}')
    globals()[f'infraHPortS{i}'] = cobra.model.infra.HPortS(infraAccPortP, type='range', name=f'1:{i2}')
    globals()[f'infraPortBlk{i}'] = cobra.model.infra.PortBlk(globals()[f'infraHPortS{i}'], fromPort=f'{i}', toPort=f'{i}', name='block2')
    globals()[f'infraRsAccBaseGrp{i}'] = cobra.model.infra.RsAccBaseGrp(globals()[f'infraHPortS{i}'])

  ''' 
  Below is the format that the APIC expects for the n+1 port, which is generated above ##

  infraHPortS2 = cobra.model.infra.HPortS(infraAccPortP, type='range', name='1:02')
  infraPortBlk2 = cobra.model.infra.PortBlk(infraHPortS2, fromPort='2', toPort='2', name='block2')
  infraRsAccBaseGrp2 = cobra.model.infra.RsAccBaseGrp(infraHPortS2)
  '''

  # Commit
  print(toXMLStr(topMo))
  c = cobra.mit.request.ConfigRequest()
  c.addMo(topMo)
  md.commit(c)


def main():
  md = connect_to_apic()
  addIntProf(md)
  
  md.logout()

if __name__ == "__main__":
    main()
