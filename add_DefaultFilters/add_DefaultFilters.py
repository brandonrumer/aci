#!/usr/local/bin/python3
""" Summary:  Logs into ACI APIC via cobraSDK and creates the several
              Filters in the common tenant. The filters that are created
              are referenced in a filters.yml file. For the purpose of
              this script, the filters are the commonly used 'literal 
              values and port numbers' that are commonly used inside 
              IOS/XE ACLs.

              getpass can be implemented in cases where this is the sole 
              script that is ran in the environment.

Requirements: 
    acicobra, pyyaml
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.0"
__email__ = "brumer@cisco.com"
__status__ = "Production"

# Import third-party modules
import yaml
# import getpass
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
  #login = input('Enter username to connect with: ')
  #passwd = getpass.getpass("Enter password: ")
  ls = cobra.mit.session.LoginSession(apicUrl, login, passwd)
  md = cobra.mit.access.MoDirectory(ls)
  md.login()
  return md


def importfilteryml(ymlfile):
  ''' yaml file should be in the following format. Note: if the protocol is udp
      then the stateful value should be blank. Fill in the bare minimum. 
    filters : 
      - name : 'cmd'
        vzentryName : 
          name : '514-tcp'
          annotation : 
          dFromPort : '514'
          dToPort : '514'
          descr :   
          etherT : 'ip'
          prot : 'tcp'
          sFromPort : 
          sToPort : 
          stateful : 'yes'
  '''  
  with open(ymlfile, "r") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
  return data


def addDefaultFilters(md, item):
  # Top level object on which operations will be made
  topDn = cobra.mit.naming.Dn.fromString('uni/tn-common/flt-cmd')
  topParentDn = topDn.getParent()
  topMo = md.lookupByDn(topParentDn)

  vzentry = item.get('vzentryName')

  vzFilter = cobra.model.vz.Filter(topMo, name=item['name'])
  vzEntry = cobra.model.vz.Entry(vzFilter, name=vzentry['name'], annotation=vzentry['annotation'], \
    dFromPort=vzentry['dFromPort'], dToPort=vzentry['dToPort'], descr=vzentry['descr'], \
      etherT=vzentry['etherT'], prot=vzentry['prot'], sFromPort=vzentry['sFromPort'], \
        sToPort=vzentry['sToPort'], stateful=vzentry['stateful'])

  # Commit
  print("This is the XML to be posted to the APIC:\n")
  print(toXMLStr(topMo))

  c = cobra.mit.request.ConfigRequest()
  c.addMo(topMo)
  md.commit(c)


def main():
  ymlfile='filters.yml'
  data = importfilteryml(ymlfile)
  md = connect_to_apic()

  for item in data.get('filters'):
    '''
    print('filter name: ' + item['name'])
    vzentry = item.get('vzentryName')
    print('Filter Subject: ' + vzentry['name'])
    '''
    addDefaultFilters(md, item)
  
  md.logout()


if __name__ == "__main__":
    main()
