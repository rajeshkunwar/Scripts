# This script takes a full backup of the mssql db and dumps to a specified location on the server with db name and today's date as the 
# dump file name. It also checks if there are any files that are older than 7 days and deletes them.
# The script also calculates how long it took to backup the database and then send an email that includes the time taken, size of the 
# backup file and backup file name

from datetime import datetime
import subprocess
import os
import sys
import send_email
import time

today = datetime.today.stftime('%m-%d-%y')
date = datetime.strptime(today, '%m-%d-%y')

db_name = 'your_db_name'
username = 'user_name'
password = 'your_secret_password'
backup_location = 'your_backup_location' # Example: 'C:\\backup\\db_backup\\'
backup_file_name = backup_location + db_name + '_' + today + '.bak' 
db_hostname = 'hostname'

command = 'SqlCmd -S %s -U %s -P %s -d master -Q "BACKUP DATABASE [%s] TO DISK = N\'%s\' WITH INIT , NOUNLOAD , NAME = N\'%s backup\', NOSKIP , STATS = 10, NOFORMAT"' %(db_hostname, username, password, db_name, backup_file_name, db_name)

start = time.time()
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
end = time.time()
time_taken = round(end - start, 2)

if process.returncode == 0:
  size = round(os.path.getsize(backup_file_name)/1024/1024/1024, 2) # Get the size in GB and round to 2 decimals.
  recipients = ['person1@example.com', 'person2@example.com'] # A list that stores the email addresses of persons that would like to receive
                                                              # email notification about the backup.
  body = """DB Backup Taken Successfully:
  File Name : %s_%s.bak
  Time Taken: %s s
  Backup File Size: %s GB""" %(db_name, today, time_taken, size)
  subject = 'DB Daily Full Backup'
  
  for recipient in recipients:
    send_email.send_email(recipient, subject=subject, body=body)
   
  files = os.listdir(backup_location)
  
  for file in files:
    created = os.path.getctime(backup_location + file)
    created = datetime.fromtimestamp(created).strftime('%m-%d-%y')
    created = datetime.strptime(created, '%m-%d-%y')
    
    if abs((created - date),days) > 7:
      os.remove(backup_location + file)
      
else:
  sys.exit()      # Here you can send email notifications about whey the backup failed by attaching the failed message on the email's body.
