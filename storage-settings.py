#!/usr/bin/env python3.6
import sys
from maas.client import connect, enum

MAAS = {
"cluster-name": ("http://X.X.X.X:5240/MAAS", "api-key"),
}

env = sys.argv[1]
c = connect(MAAS[env][0], apikey=MAAS[env][1])

f = open('{}-storage_conf'.format(env),'w'); sys.stdout = f

for machine in c.machines.list():
        disks=[]
        mtags = machine.tags
        if machine.status.name is 'READY':


            for devices in machine.block_devices:

                if devices.model == "os-device-model":
                    disks.append(devices.name)

            for tag in mtags:


                if tag.name == "server-name":

                    machine.restore_storage_configuration()

                    os_disk2 = machine.block_devices.get_by_name(disks[1])
                    os_disk2.set_as_boot_disk()

                    os_disk2p = os_disk2.partitions.create ({"size": [""]})

                    os_disk1 = machine.block_devices.get_by_name(disks[0])
                    os_disk1.set_as_boot_disk()


                    md0 = machine.raids.create(name="md0",level="raid-1",devices=[os_disk1,os_disk2p],spare_devices=[])

                    md0.virtual_device.format("ext4")
                    md0.virtual_device.mount("/")

                    nvme0n1 = machine.block_devices.get_by_name("nvme0n1")
                    nvme1n1 = machine.block_devices.get_by_name("nvme1n1")

                    md1 = machine.raids.create(name="md1",level="raid-0",devices=[nvme0n1,nvme1n1],spare_devices=[])

                    md1.virtual_device.format("xfs")
                    md1.virtual_device.mount("/data")

                    print(machine.hostname,"\n",md0.name,"->",md0.level.value,disks[0],disks[1],"\n",md1.name,"->",md1.level.value,nvme0n1.name,nvme1n1.name)




                if tag.name == "server-name":

                    machine.restore_storage_configuration()

                    os_disk2 = machine.block_devices.get_by_name(disks[1])
                    os_disk2.set_as_boot_disk()

                    os_disk2p = os_disk2.partitions.create ({"size": [""]})

                    os_disk1 = machine.block_devices.get_by_name(disks[0])
                    os_disk1.set_as_boot_disk()

                    md0 = machine.raids.create(name="md0",level="raid-1",devices=[os_disk1,os_disk2p],spare_devices=[])

                    md0.virtual_device.format("ext4")
                    md0.virtual_device.mount("/")

                    nvme0n1 = machine.block_devices.get_by_name("nvme0n1")
                    nvme0n1.format("ext4")
                    nvme0n1.mount("/var/lib/etcd")

                    nvme1n1 = machine.block_devices.get_by_name("nvme1n1")
                    nvme1n1.format("ext4")
                    nvme1n1.mount("/var/lib/rook")

                    print(machine.hostname,"\n",md0.name,"->",md0.level.value,disks[0],disks[1])
