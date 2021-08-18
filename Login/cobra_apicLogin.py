#!/usr/local/bin/python3

""" Summary: Logs into ACI APIC via cobraSDK

Requirements: 
    acicobra, acimodel
"""

__author__ = "Brandon Rumer"
__version__ = "1.0.1"
__email__ = "brumer@cisco.com"
__status__ = "Production"


from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def apicLogin(DefaultApicUrl, login, passwd):
    DefaultApicUrl = 'https://' + DefaultApicUrl
    loginSession = LoginSession(DefaultApicUrl, login, passwd)
    moDir = MoDirectory(loginSession)
    moDir.login()
    return moDir


def main():
    # Statically specify the APIC URL, if not executing script via CLI
    DefaultApicUrl = 'sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = '!v3G@!4@Y'
        
    #login = input('Enter username to connect with: ')
    #passwd = getpass.getpass("Enter password: ")
    
    moDir=apicLogin(DefaultApicUrl, login, passwd)
    moDir.logout()


if __name__ == "__main__":
    main()
