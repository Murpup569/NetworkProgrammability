#!/usr/bin/env python

"""
NETWORK AUTOMATION

This script will configure all the VLANs specified in
the vlan.txt file on every network device in inventory.txt.
Every other line in vlan.txt should be the VLAN ID and
underneath that the VLAN Name.

This script will use SSH. Please have that configured
on the network devices before hand.
"""

__author__ = "Ryan Murray"
__version__ = "2.0"
__maintainer__ = "Ryan Murray"
__email__ = "ryan.murray.570@gmail.com"
__status__ = "Prototype"

import getpass
import os
import paramiko
import sys
import time

# Verifying that an inventory file exists!
exists1 = os.path.isfile('inventory.txt')
if not exists1:
    print('Inventory file not found!')
    sys.exit()

# Verifying that a vlan file exists!
exists2 = os.path.isfile('vlan.txt')
if not exists2:
    print('VLAN file not found!')
    sys.exit()

# Asks user for credentials
user = input("Username: ")
password = getpass.getpass()

# Sets the variable ssh_client to the ssh module in paramiko
SshClient = paramiko.SSHClient()
SshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Inputs each line without a comment into an array called hosts
hosts = []
with open('inventory.txt') as fh:
    for line in fh:
        if '#' not in line:
            hosts.append(line)

# Inputs each line without a comment into an array called vlans
vlans = []
vlanID = []
vlanName = []
counter = 2
with open('vlan.txt') as fh:
    for line in fh:
        mod = counter % 2
        if mod == 0:
            vlanID.append(line.strip('\n'))
        else:
            vlanName.append(line.strip('\n'))
        counter += 1

for i in range(len(hosts)):

    # Logs into the networking device
    SshClient.connect(hostname=hosts[i], username=user, password=password)
    remote_connection = SshClient.invoke_shell()

    # Prints the IP Address its connecting to
    print('Configuring switch', hosts[i])

    # Sets the terminal length to the maximum so all output comes out at once
    remote_connection.send("terminal length 0\n")
    remote_connection.send("conf t\n")

    # Configures vlans on each network device in inventory.txt
    for v in range(len(vlanID)):
        remote_connection.send("vlan " + vlanID[v] + "\n")
        remote_connection.send("name " + vlanName[v] + "\n")
        time.sleep(0.5)

    # Exits the network device and saves the configuration
    remote_connection.send("end\n")
    remote_connection.send("wr\n")
    remote_connection.send("exit\n")

    SshClient.close
