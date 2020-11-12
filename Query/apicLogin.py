#!/usr/local/bin/python3

""" Summary: Logs into APIC and generates login cookie.

    getpass can be implemented in cases where this is the sole 
    script that is ran in the environment.
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.3"
__email__ = "brumer@cisco.com"
__status__ = "Production"


import requests, json, sys
#import getpass 

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def aaaLogin(apicUrl, login, passwd):
    credentials = {'aaaUser':
                    {'attributes':
                        {'name': login, 'pwd': passwd }
                    }
        }

    base_url = f"https://{apicUrl}/api/"
    login_url = base_url + 'aaaLogin.json'
    json_credentials = json.dumps(credentials)

    try:
        # Post & get the response
        post_response = requests.post(login_url, data=json_credentials, verify=False)
        # Dump the text of the response to a json object
        post_response_json = json.loads(post_response.text)
        if post_response.ok:
            # Extract the token
            token = post_response_json['imdata'][0]['aaaLogin']['attributes']['token']
            # Generate a cookie dict to be used in the POST header
            cookies = {}
            cookies['APIC-Cookie'] = token
            #print(cookies)
            return cookies
        else:
            print('Connection Error. Wrong credentials? Terminating.\n')
            sys.exit(1)
    except requests.ConnectionError:
        print('Connection Error. Check APIC URL. Terminating.\n')
        sys.exit(1)


def main():
    apicUrl = 'sandboxapicdc.cisco.com'

    ### Coment/uncomment the below static entries if using getpass ###
    login = 'admin'
    passwd = 'ciscopsdt'
    #login = input('Enter username to connect with: ')
    #passwd = getpass.getpass("Enter password: ")

    cookies = aaaLogin(apicUrl, login, passwd)
    print(f"apicLogin cookie: {cookies}")

if __name__ == "__main__":
    main()
