#!/usr/local/bin/python3.6

import os
import datetime
import time
import subprocess
import send_email

date = datetime.date.today().strftime('%m-%d-%y')

# converting the above date so that the difference of two dates can be calculated.
today = datetime.datetime.strptime(date, '%m-%d-%y')

backup_path = '/root/nagios_backup'
backup_cmd = 'tar -cvzpf %s/nagios-%s.tar.gz /usr/local/nagios' %(backup_path, date)

process = subprocess.Popen(backup_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
output, err = process.communicate()

if process.returncode == 0:
        recipients = ['email1@address.com', 'email2@address.com']
        body = 'Nagios Full Backup Taken Successfully: nagios-%s.tar.gz' %date
        subject = 'Nagios Daily Full Backup'

        for recipient in recipients:
                send_email.send_email(recipient, body=body, subject=subject)


# os.listdir returns a list.
files = os.listdir(backup_path)

for file in files:
        created = os.path.getctime(backup_path + '/' + file)
        created = datetime.datetime.fromtimestamp(created).strftime('%m-%d-%y')
        created = datetime.datetime.strptime(created, '%m-%d-%y')

        # delete backups that are older than 7 days.
        if abs((created - today).days) > 7:
                os.remove(backup_path + '/' + file)
