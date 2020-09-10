#!/usr/local/bin/python3

""" Summary: Logs into ACI APIC via cobraSDK

Requirements: 
    acicobra, acimodel
"""

from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession

# Disable insecure certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def apicLogin():
    apicUrl = 'https://sandboxapicdc.cisco.com'
    login = 'admin'
    passwd = 'ciscopsdt'
    loginSession = LoginSession(apicUrl, login, passwd)
    moDir = MoDirectory(loginSession)
    moDir.login()
    return moDir


def main():
    moDir=apicLogin()
    moDir.logout()


if __name__ == "__main__":
    main()
