#!/usr/local/bin/python3.6

# Author: Raj
# Version: 1.0

import subprocess
import codecs
import datetime
import send_email

def snapshot(*args):
        vms = []
        email_recipients = []
        today = datetime.date.today().strftime('%m-%d-%y')

        # separate the arguments passed into vms and email addresses.
        for arg in args:

                if '.com' in arg:
                        email_recipients.append(arg)
                else:
                        vms.append(arg)

        # first get the server pool for the vms because that's where the snapshot will be created.
        for vm in vms:
                command = 'sshpass -p "password" ssh admin@hostname -p 10000 show Vm name=%s' %vm
                process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

                for line in process.stdout:

                        # line is a byte like object and hence needs to be converted to string.
                        if 'Server Pool' in codecs.decode(line):
                                pool = codecs.decode(line).split()
                                pool = pool[4].strip('[]')

                # now get the snapshots for the vm if any.
                command = 'sshpass -p "password" ssh admin@hostname -p 10000 list Vm | grep "name:" | grep %s-SNAP' %vm
                process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                snapshots = []

                for line in process.stdout:
                        line = codecs.decode(line).split()
                        snapshots.append(line[1][5:])

                # for the snapshot get the vm disk mappings and disk ids and delete them.
                disk_mappings = []
                disk_ids = []

                for snapshot in snapshots:
                        disk_command = 'sshpass -p "password" ssh admin@hostname -p 10000 show Vm name=%s' %snapshot
                        disk_process = subprocess.Popen(disk_command, stdout=subprocess.PIPE, shell=True)

                        for line in disk_process.stdout:

                                if 'VmDiskMapping' in codecs.decode(line):
                                        line = codecs.decode(line).split()
                                        disk_mappings.append(line[3])
                                        disk_ids.append(line[8].strip('()]'))

                        # delete the vm disk mappings
                        for disk_mapping in disk_mappings:
                                disk_map_del_command = 'sshpass -p "password" ssh admin@hostname -p 10000 delete VmDiskMapping id=%s' %disk_mapping
                                disk_map_del_process = subprocess.Popen(disk_map_del_command, stdout=subprocess.PIPE, shell=True)
                                disk_map_del_process.wait()

                        # delete the virtual disks
                        for disk_id in disk_ids:
                                disk_del_command = 'sshpass -p "password" ssh admin@hostname -p 10000 delete VirtualDisk id=%s' %disk_id
                                disk_del_process = subprocess.Popen(disk_del_command, stdout=subprocess.PIPE, shell=True)
                                disk_del_process.wait()

                        # delete the snapshot
                        del_snapshot_command = 'sshpass -p "password" ssh admin@hostname -p 10000 delete Vm name=%s' %snapshot
                        del_snapshot_process = subprocess.Popen(del_snapshot_command, stdout=subprocess.PIPE, shell=True)
                        del_snapshot_process.wait()

                # take the new snapshot now
                snapshot_command = 'sshpass -p "password" ssh admin@hostname -p 10000 clone Vm name=%s destType=Vm destName=%s-SNAP-%s serverPool=%s' %(vm, vm, today, pool)
                snapshot_process = subprocess.Popen(snapshot_command, stdout=subprocess.PIPE, shell=True)
                snapshot_process.wait()

                # move the snapshot to the unassigned vm folder
                move_command = 'sshpass -p "password" ssh admin@hostname -p 10000 migrate Vm name=%s-SNAP-%s' %(vm, today)
                move_process = subprocess.Popen(move_command, stdout=subprocess.PIPE, shell=True)
                move_process.wait()

                # send the email
                for recipient in email_recipients:
                        send_email.send_email(recipient, body='Snapshot for ' + vm + ' :   ' + vm + '-SNAP-' + today + ' ' + 'taken successfully', subject='Snapshots')
