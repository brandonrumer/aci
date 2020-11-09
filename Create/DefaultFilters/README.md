# add_DefaultFilters.py
Logs into ACI APIC via cobraSDK and creates the several filters in the common tenant. 

## Summary
The filters that are created are referenced in a filters.yml file. For the purpose of this script, the filters are the commonly used 'literal values and port numbers' that are commonly used inside IOS/XE ACLs.

getpass can be implemented in cases where this is the sole script that is ran in the environment.

The yaml file should be in the following format:
```
---
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
  - name: 'domain'
    vzentryName : 
      name : '53-tcp'
      dFromPort : '53'
      annotation : 
      dToPort : '53'
      descr : 
      etherT : 'ip'
      prot : 'tcp'
      sFromPort : 
      sToPort : 
      stateful : 'yes'
```          
Note: if the protocol is udp then the stateful value should be blank. Each Filter Entry needs a new section. Fill in the bare minimum. 

### Prerequisites
acicobra, pyyaml

#### cobraSDK prerequisites
ply, future, certificate, idna, requests
