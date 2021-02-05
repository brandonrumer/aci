# bACI
Useful python scripts when interacting with an ACI fabric. 

# Description
bACI is a collection of various python scripts that you can use to interact with an ACI fabric. The scripts are organized in such a way that they can be ran as standalone scripts or by using pACI.py as an entrypoint. Because of the ability to run scripts as standalone some functions are copied into sub-folders because it's easier than dealing with python absolute or relative imports.  

## Usage
```
$ python bACI.py

optional arguments:
  -h, --help            show this help message and exit
  -q query, --query query
                        What to query. Values can be:
                        tenant, epg, bd, endpoints, leaf, lldp_info
  -c create, --create create
                        What to create. Values can be:
                        filters -  Use --file to specificy yaml file input
                        intprof -  Use "--option Leaf-201,1,48" , where Leaf-201 is profile name, 1 is
                                   starting interface, and 48 ending interface
                        tenant -   Use "--option Tenant1" , where Tenant1 is tenant to be created
                        vlanpool - Use --file to specify a csv file input
                                   Use "--option VLANPoolName,static" to define pool name and type (no space)
  -f file, --file file  Specifies a file to use for the action. Current supported actions
                        that can be used with this: default_filters, vlanpool
  -t target, --target target
                        ACI Fabric IP or hostname.
  -o option, --option option
                        Values for various creates/queries.
```

## Examples to create objects
Below are examples for certain create commands when running bACI.py on a Windows host

### Create Filters in common tenant from yml file
For the ACI fabric sandboxapicdc.cisco.com, create filters specified in filters.yml file 
```
python .\bACI.py -c filters -f .\create\collateral\filters.yml -t sandboxapicdc.cisco.com
```
### Create Leaf Interface Profiles
For the ACI fabric sandboxapicdc.cisco.com , create a switch interface profile named Leaf-1, and create interface selectors 1-48, labeled 1:01, 1:02, etc...
```
python .\bACI.py -c intprof --option Leaf-1,1,48 -t sandboxapicdc.cisco.com
```
### Create tenant
For the ACI fabric sandboxapicdc.cisco.com, create Tenant1 
```
python .\bACI.py -c tenant --option Tenant1
```
### Create VLAN Pool
For the ACI fabric sandboxapicdc.cisco.com, create a static VLAN pool with the IDs specified in the vlans.csv file 
```
python .\bACI.py -c vlanpool -f .\create\collateral\vlans.csv -o ScriptVLAN_pool,static -t sandboxapicdc.cisco.com
```

## Prerequisites
I am still working on standardizing the sub-module's dependancies. For now, the following are generally required.<br>
prettyprint (pprintpp) <br>
prettytable (prettytable) <br>
tabulate <br>
cobraSDK <br>

### References
https://aci-prog-lab.ciscolive.com/lab/pod21
<br />
https://developer.cisco.com/docs/aci/#!sandbox/aci-sandboxes