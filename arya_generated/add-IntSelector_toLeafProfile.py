#!/usr/bin/env python
'''
Autogenerated code using arya.py
Original Object Document Input: 

url: https://sandboxapicdc.cisco.com/api/node/mo/uni/infra/nprof-leaf_1.json
payload{"infraRsAccPortP":{"attributes":{"tDn":"uni/infra/accportprof-Leaf101","status":"created,modified"},"children":[]}}

raise RuntimeError('Please review the auto generated code before ' +
                    'executing the output. Some placeholders will ' +
                    'need to be changed')


Validated working BDR 20200911
  Note: I had to change line 443 in arya.py:
    https://github.com/datacenter/arya/issues/12
  The topMo also required manual entry because of the POST URL
'''

### Associates an Interface Selector with a Leaf Profile ###

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.infra
from cobra.internal.codec.xmlcodec import toXMLStr

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://sandboxapicdc.cisco.com', 'admin', 'ciscopsdt')
md = cobra.mit.access.MoDirectory(ls)
md.login()

##################################################################
# the top level object on which operations will be made
# Replace the text below with the dn of your top object
topMo = md.lookupByDn('uni/infra/nprof-leaf_1')
##################################################################

# build the request using cobra syntax
infraRsAccPortP = cobra.model.infra.RsAccPortP(topMo, tDn='uni/infra/accportprof-Leaf101')


# commit the generated code to APIC
print(toXMLStr(topMo))
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
md.commit(c)

