#!/usr/local/bin/python3

""" Summary:  Logs into ACI APIC and creates a VLAN Pool. 

    Description: 
        The VLAN Pool must be specified in the python code. 
        This script will raise a GUI prompt to ask for the file of 
        VLANs. The file should only have VLAN numbers, each on a 
        different line with no seperator other than a line break. 

    Requirements: 
        apicLogin.py
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.0"
__email__ = "brumer@cisco.com"
__status__ = "Production"

#import getpass
import requests, json, time
import tkinter as tk
from tkinter import filedialog

# Reuse apicLogin code
from apicLogin import aaaLogin

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def createVLANPool(base_url, cookies, vlanpoolname, assignmethod, json_object):
    api_url = f"/api/node/mo/uni/infra/vlanns-[{vlanpoolname}]-{assignmethod}.json"
    full_url = base_url + api_url

    # Post the data
    response_data = requests.post(full_url, cookies=cookies, data=json_object, verify=False)

    # Verify it worked
    if response_data.ok:
        # Wait for tenant to be added all the way
        time.sleep(3)
        print('Pool created.')
    else:
        # The initial HTTP POST failed; print details
        print(f"Device addition failed with code {response_data.status_code}")
        print(f"Failure body: {response_data.text}")


def main():
    apicUrl = 'sandboxapicdc.cisco.com'
    base_url = f"https://{apicUrl}"

     ###### Name of VLAN Pool ######
    vlanpoolname = 'TEST_Pool'
    assignmethod = 'dynamic'  # set 'dynamic' or 'static'
    ################################

    ''' Ask user what file to use. File should have only one 
        column with only IPs in a single column. Or, just statically
        set the filename. '''
    vlanlist = []
    somefile = tk.Tk()
    somefile.withdraw()
    filename = filedialog.askopenfilename()
    
    # Open the file and strips blank lines
    with open(filename, "r") as file_in:
        for line in file_in:
            if not line.isspace():
                line = line.replace('\n', '')
                vlanlist.append(line)

    # Create the JSON child objects (vlan block)
    childrenkey = []
    for vlan in vlanlist:
        childrenkey.append({
                "fvnsEncapBlk":{
                    "attributes":{
                        "dn":f"uni/infra/vlanns-[{vlanpoolname}]-{assignmethod}/from-[vlan-{vlan}]-to-[vlan-{vlan}]",
                        "from":f"vlan-{vlan}",
                        "to":f"vlan-{vlan}",
                        "rn":f"from-[vlan-{vlan}]-to-[vlan-{vlan}]"
                    }
                }
        })

    # Put all the JSON together
    data = {
    "fvnsVlanInstP":{
        "attributes":{
            "dn":f"uni/infra/vlanns-[{vlanpoolname}]-{assignmethod}",
            "name":vlanpoolname,
            "rn":f"vlanns-[{vlanpoolname}]-{assignmethod}"
        },
        "children":childrenkey
    }
    }

    # Create the JSON object from the data 
    json_object = json.dumps(data)
    #print(json_object)

    # Get the authorization cookie from the APIC
    cookies = aaaLogin()

    # Create the pool
    responsedata = createVLANPool(base_url, cookies, vlanpoolname, assignmethod, json_object)


if __name__ == "__main__":
    main()

