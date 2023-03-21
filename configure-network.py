#!/usr/bin/env python3.6

from maas.client import connect, enum
import csv,sys

MAAS = {
"server": ("http://.x.x.x.x:5240/MAAS", "maas-key", "x.x.x./x", "x.x.x./x"),}


env = sys.argv[1]
c = connect(MAAS[env][0], apikey=MAAS[env][1])

data_subnet = c.subnets.get(MAAS[env][2])
pxe_subnet = c.subnets.get(MAAS[env][3])

datalist = {}
pxelist = {}

f = open('{}-network_conf'.format(env),'w'); sys.stdout = f

with open(sys.argv[2], "r") as csvFile:
    reader = csv.reader(csvFile)

    for row in reader:

        datalist[row[6]] = row[9]
        pxelist[row[6]] = row[8]

for machine in c.machines.list():
    mtags = machine.tags
    if machine.status.name is 'READY':


        for tag in mtags:
            if tag.name == "name":

                machine.restore_networking_configuration()

                eno1 = machine.interfaces.get_by_name("eno1")
                eno2 = machine.interfaces.get_by_name("eno2")
                enp134s0f0 = machine.interfaces.get_by_name("enp134s0f0")
                enp134s0f1 = machine.interfaces.get_by_name("enp134s0f1")

                eno2.params = {"mtu": 9000}
                eno2.save()
                enp134s0f0.params = {"mtu": 9000}
                enp134s0f0.save()

                eno1.disconnect()
                eno2.disconnect()
                enp134s0f0.disconnect()
                enp134s0f1.disconnect()

                eno1.links.create(enum.LinkMode.STATIC, subnet=pxe_subnet, ip_address = pxelist[machine.hostname])
                new_bond = machine.interfaces.create( enum.InterfaceType.BOND, name="bond0", mtu=9000, parents={eno2,enp134s0f0}, bond_mode="802.3ad", bond_lacp_rate="slow", bond_xmit_hash_policy="layer3+4", bond_miimon="100")
                bridge_nic = machine.interfaces.create(enum.InterfaceType.BRIDGE, name="cnio0", mtu=9000, parent=machine.interfaces.get_by_name("bond0"))
                bridge_nic.links.create(enum.LinkMode.STATIC, subnet=data_subnet, ip_address = datalist[machine.hostname])

                print(machine.hostname,"\n",bridge_nic.name,"->",datalist[machine.hostname],"\n",eno1.name,"->",pxelist[machine.hostname])

            if tag.name == "tagname":

                machine.restore_networking_configuration()

                eno1 = machine.interfaces.get_by_name("eno1")
                eno2 = machine.interfaces.get_by_name("eno2") 
                enp216s0f0 = machine.interfaces.get_by_name("enp216s0f0")
                enp216s0f1 = machine.interfaces.get_by_name("enp216s0f1")

                enp216s0f0.params = {"mtu": 9000}
                enp216s0f0.save()
                enp216s0f1.params = {"mtu": 9000}
                enp216s0f1.save()

                eno1.disconnect()
                eno2.disconnect()
                enp216s0f0.disconnect()
                enp216s0f1.disconnect()

                eno1.links.create(enum.LinkMode.STATIC, subnet=pxe_subnet, ip_address = pxelist[machine.hostname])
                new_bond = machine.interfaces.create( enum.InterfaceType.BOND, name="bond0", mtu=9000, parents={enp216s0f0,enp216s0f1}, bond_mode="802.3ad", bond_lacp_rate="slow", bond_xmit_hash_policy="layer3+4", bond_miimon="100")
                bridge_nic = machine.interfaces.create(enum.InterfaceType.BRIDGE, name="cnio0", mtu=9000, parent=machine.interfaces.get_by_name("bond0"))
                bridge_nic.links.create(enum.LinkMode.STATIC, subnet=data_subnet, ip_address = datalist[machine.hostname])

                print(machine.hostname,"\n",bridge_nic.name,"->",datalist[machine.hostname],"\n",eno1.name,"->",pxelist[machine.hostname])
