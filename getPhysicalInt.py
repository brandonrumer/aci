#!/usr/local/bin/python3

""" Summary: Gets physical interface list of Nexus switches in the ACI fabric

Requirements: 
    prettytable

"""

__author__ = "Brandon Rumer"
__version__ = "1.0.0"
__email__ = "brumer@cisco.com"
__status__ = "Production"


import requests, json, re, operator
from prettytable import PrettyTable 

# Disable insecure certificate warning
requests.packages.urllib3.disable_warnings()


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

    # Generate a cookie dict
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
    table.field_names = ['dn','Port','Node']
    for row in data:
        try:
            node = re.search(r'node-\d\d\d', str(row["dn"])).group(0)
        except AttributeError:
            node = ''
        table.add_row([row['dn'],row['id'],node])
    return(table)


def main():
    cookies = aaaLogin()
    endpoint_data = getInt(cookies)
    
    # Cleanup the data
    table = cleanupendpoints(endpoint_data)
    print(table.get_string(sort_key=operator.itemgetter(1, 0), sortby="Node"))

if __name__ == "__main__":
    main()
