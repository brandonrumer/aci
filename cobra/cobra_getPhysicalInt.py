#!/usr/local/bin/python3

""" Summary: Gets physical interface status of ACI Nexus switches

Requirements: 
    acicobra, acimodel

"""

__author__ = "Mike Timm, Toru Okatsu, Brandon Rumer"
__version__ = "0.0.1"
__email__ = "brumer@cisco.com"
__status__ = "Development"

import requests, json, pprint
from prettytable import PrettyTable


# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


apicUrl = 'sandboxapicdc.cisco.com'
login = 'admin'
passwd = 'ciscopsdt'
base_url = f"https://{apicUrl}/api/"


def aaaLogin():
    credentials = {'aaaUser':
                    {'attributes':
                        {'name': login, 'pwd': passwd }
                    }
        }

    base_url = f"https://{apicUrl}/api/"
    login_url = base_url + 'aaaLogin.json'
    json_credentials = json.dumps(credentials)

    # Post & get the response
    post_response = requests.post(login_url, data=json_credentials, verify=False)

    # Dump the text of the response to a json object
    post_response_json = json.loads(post_response.text)

    # Extract the token
    token = post_response_json['imdata'][0]['aaaLogin']['attributes']['token']

    # Generate a cookie dict (why?)
    cookies = {}
    cookies['APIC-Cookie'] = token
    return cookies


def getInt(cookies):
    request_url = 'node/class/l1PhysIf.json'
    response_data = requests.get(base_url + request_url, cookies=cookies, verify=False)
    endpoint_data = json.loads(response_data.text)
    return endpoint_data


def cleanupendpoints(endpoint_data):
    # Cleanup the endpoint info
    fields = ['dn', 'id']
    data = []

    for endpoint in endpoint_data['imdata']:
        for stuff in endpoint['l1PhysIf'].items():
            line_dict = {}
            for field in fields:
                line_dict[field] = stuff[1][field]
            data.append(line_dict)

    table = PrettyTable()
    table.field_names = ['dn','Port']
    for row in data:
        table.add_row([row['dn'],row['id']])
    return(table)


def main():
    cookies = aaaLogin()
    endpoint_data = getInt(cookies)
    
    # Cleanup the endpoint
    table = cleanupendpoints(endpoint_data)

    print(table)



    '''
    # Dump the text of the response to a json object
    #endpointdata_json = json.loads(endpoint_data)
    print(f'endpointdata_json: {endpoint_data[0]}')
    quit()
    # Extract the interface
    interface = endpointdata_json['imdata']['l1PhysIf']['attributes']['id']
    #interface = endpointdata_json['imdata'][0]
    pprint(interface)
    '''


    

    '''
    for i in endpoint_data['imdata']:
        #for j in i:['l1PhysIf']:
        #    print(j)
        print(i['l1PhysIf'['attributes'['id']]])
    '''



if __name__ == "__main__":
    main()
