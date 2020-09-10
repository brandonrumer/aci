#!/usr/local/bin/python3

""" Summary: Gathers all the physical inventory

Requirements: 
    acitoolkit, prettytable
"""

import acitoolkit.acitoolkit as aci
import sys
from prettytable import PrettyTable
from acitoolkit import Session, Credentials
from acitoolkit.aciphysobject import Pod

# Import my own modules
from acitoolkit_login import apicLogin

def print_inventory(item):
    """
    Recursive print routine
    """
    for child in item.get_children():
        print_inventory(child)
    print(item.info())


def getAllNodes(session):
    # List of classes to get and print
    # Print the inventory of each Pod
    pods = Pod.get(session)
    for pod in pods:
        pod.populate_children(deep=True)
        pod_name = 'Pod: %s' % pod.name
        print(pod_name)
        print('=' * len(pod_name))
        print_inventory(pod)


if __name__ == "__main__":
    try:
        session = apicLogin()
        AllNodes = getAllNodes(session)
    except KeyboardInterrupt:
        print('Keyboard interrupt. Quitting...')
        quit()
    