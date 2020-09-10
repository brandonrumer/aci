#!/usr/local/bin/python3

""" Summary: Gathers all connected endpoints

Requirements: 
    acicobra, acimodel, arya
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


def getuni(moDir):
    uniMo = moDir.lookupByDn('uni')
    # Use the connected moDir queries and configuration...
    tenant1Mo = moDir.lookupByClass("fvTenant")
    print(tenant1Mo)
    return


def main():
    try: 
        moDir=apicLogin()
        getuni(moDir)
    except KeyboardInterrupt:
        print('Keyboard interrupt. Quitting...')
        quit()
    moDir.logout()


if __name__ == "__main__":
    main()

