# NetworkProgrammability

This script will configure all the VLANs specified in
the vlan.txt file on every network device in inventory.txt.
Every other line in vlan.txt should be the VLAN ID and
underneath that the VLAN Name.

###### Requirements
This script will use SSH. Please have that configured
on the network devices before hand.
###### Libaraies
Paramiko is used in this script. I created requirements.txt to make it easy for you!
