#!/usr/bin/env python
'''
Autogenerated code using arya.py
Original Object Document Input: 
{"infraHPortS":{"attributes":{"dn":"uni/infra/accportprof-Leaf101/hports-1:04-typ-range","name":"1:04","rn":"hports-1:04-typ-range","status":"created,modified"},"children":[{"infraPortBlk":{"attributes":{"dn":"uni/infra/accportprof-Leaf101/hports-1:04-typ-range/portblk-block2","fromPort":"4","toPort":"4","name":"block2","rn":"portblk-block2","status":"created,modified"},"children":[]}},{"infraRsAccBaseGrp":{"attributes":{"status":"created,modified"},"children":[]}}]}}

raise RuntimeError('Please review the auto generated code before ' +
                    'executing the output. Some placeholders will ' +
                    'need to be changed')


Validated working BDR 20200911
  Note: I had to change line 443 in arya.py:
    https://github.com/datacenter/arya/issues/12
'''

### Adds a single interface selector to an existing Interface Profile ###

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.naming
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

# the top level object on which operations will be made
# Confirm the dn below is for your top dn
topDn = cobra.mit.naming.Dn.fromString('uni/infra/accportprof-Leaf101/hports-1:04-typ-range')
topParentDn = topDn.getParent()
topMo = md.lookupByDn(topParentDn)

# build the request using cobra syntax
infraHPortS = cobra.model.infra.HPortS(topMo, name='1:04', type='range') # Arya didn't add 'range'
infraPortBlk = cobra.model.infra.PortBlk(infraHPortS, fromPort='4', toPort='4', name='block2')
infraRsAccBaseGrp = cobra.model.infra.RsAccBaseGrp(infraHPortS)


# commit the generated code to APIC
print(toXMLStr(topMo))
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
md.commit(c)

