#!/usr/bin/env python3

""" Summary:  Logs into ACI APIC via cobraSDK and creates the Interface 
              Profile interface selectors for every interface on the switch.
              
              Code was partially generated via arya.

              getpass can be implemented in cases where this is the sole 
              script that is ran in the environment.

Requirements: 
    acicobra, acimodel
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.2"
__email__ = "brumer@cisco.com"
__status__ = "Production"

# Import built-in modules

# Import third-party modules
import cobra.mit.access
import cobra.mit.naming
import cobra.mit.request
import cobra.mit.session
import cobra.model.infra
from cobra.internal.codec.xmlcodec import toXMLStr
import argparse
# import getpass


# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def apicLogin(DefaultApicUrl, login, passwd):
  DefaultApicUrl = 'https://' + DefaultApicUrl
  ls = cobra.mit.session.LoginSession(DefaultApicUrl, login, passwd)
  md = cobra.mit.access.MoDirectory(ls)
  md.login()
  return md


def addIntProf(md, args):
  # The next two try blocks are for the bACI input while accounting for a standalone run option.
  try: 
    profile, start, end = args.option.split(',')
  except:
    pass
  try:
    profile = args.profile
    start = args.start
    end = args.end
  except:
    pass

  # Top level object on which operations will be made
  topDn = cobra.mit.naming.Dn.fromString(f'uni/infra/accportprof-{profile}')   #<-- Actual Switch to tie it to
  topParentDn = topDn.getParent()
  topMo = md.lookupByDn(topParentDn)

  # Begin building the request using cobra syntax
  infraAccPortP = cobra.model.infra.AccPortP(topMo, name=profile)   #<--Switch Profile Name

  # Pre-load the first interface because it doesn't actually have a number in the infraHPortS variable (just easier)
  infraHPortS = cobra.model.infra.HPortS(infraAccPortP, type='range', name=f'1:0{start}')
  infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, fromPort=f'{start}', toPort=f'{start}', name='block2')
  infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS)

  # Create the rest of the interfaces, using a leading 0 for single digits.
  nextint = int(start) + 1
  end = int(end) + 1
  for i in (range(nextint,end)):
    i2 = ('%02d' % i)
    #print(f'i:{i}, i2:{i2}')
    globals()[f'infraHPortS{i}'] = cobra.model.infra.HPortS(infraAccPortP, type='range', name=f'1:{i2}')
    globals()[f'infraPortBlk{i}'] = cobra.model.infra.PortBlk(globals()[f'infraHPortS{i}'], fromPort=f'{i}', toPort=f'{i}', name='block2')
    globals()[f'infraRsAccBaseGrp{i}'] = cobra.model.infra.RsAccBaseGrp(globals()[f'infraHPortS{i}'])

  ''' 
  Below is the format that the APIC expects for the n+1 port, which is generated above.

  infraHPortS2 = cobra.model.infra.HPortS(infraAccPortP, type='range', name='1:02')
  infraPortBlk2 = cobra.model.infra.PortBlk(infraHPortS2, fromPort='2', toPort='2', name='block2')
  infraRsAccBaseGrp2 = cobra.model.infra.RsAccBaseGrp(infraHPortS2)
  '''

  # Commit
  print("This is the XML to be posted to the APIC:\n")
  print(toXMLStr(topMo))
  c = cobra.mit.request.ConfigRequest()
  c.addMo(topMo)
  md.commit(c)


def main():
  # Statically specify the APIC URL, if not executing script via CLI
  DefaultApicUrl = 'sandboxapicdc.cisco.com'
  login = 'admin'
  passwd = 'ciscopsdt'
  #login = input('Enter username to connect with: ')
  #passwd = getpass.getpass("Enter password: ")

  # Login to the APIC using CobraSDK
  md=apicLogin(DefaultApicUrl, login, passwd)

  # Use arg parse to capture any the CLI arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--profile', '-p', action='store', 
    help="The leaf profile name to create (Leaf-201)")
  parser.add_argument('--start', '-s', action='store', 
    help="The starting interface number (e1/01 would be '1')")
  parser.add_argument('--end', '-e', action='store', 
    help="The ending interface number (e1/48 would be '48')")
  args = parser.parse_args()
  
  if args.profile == None:
    args.profile = 'Leaf101'
  if args.start == None:
    args.start = '1'
  if args.end == None:
    args.end = '48'

  addIntProf(md, args)
  
  md.logout()


if __name__ == "__main__":
    main()
