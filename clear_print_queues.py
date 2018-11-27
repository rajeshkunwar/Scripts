#!/usr/local/bin/python3.7

import subprocess
import codecs
from datetime import datetime

# Command to list the printer queues and get the rows except 2,3 and 10. Row 1 has the printer info and rows 4-9 form a date.
# Example:
# Printer01-33401   user    56320   Mon 26 Nov 2018 01:07:55 PM PST
# Printer02-33402   user    51200   Mon 26 Nov 2018 01:11:48 PM PST
# Printer03-33403   user    51200   Mon 26 Nov 2018 01:25:34 PM PST
command = "lpstat -o | awk '{$2=$3=$10=\"\"; print $0}'"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output = process.communicate()

# Split the output at each new line. Each line ha,s the printer name and print
# job number separated by dash(-) and the date.
for line in output:
  line = codecs.decode(line) # get rid of the \n \r characters in the output.
  line  line.split('\n')
  
  # For each line that has the printer name, job number and the date, convert it to a dict(key, value)
  # where the key is the printer name and job number separated by dash and value is the datetime.
  for i in line:
    
    # If the value is empty (usually the last line is empty), ignore it.
    if not i:
      pass
    
    else:
      store = dict([i.split(''), 1)]) # Now each entry is a dict.
      
      # Finding if the print job has been there for longer that two hours.
      for key, value in store.items():
        two_hours_diff = datetime.today() - datetime.strptime(value.strip(), '%a %d %b %Y %I:%M:%S %p')
        
        # If the print job has been queued for longer than 2 hours then split the key which is the printer name and
        # print job number separated by dash. The key will be split at the dash and we will only grab the print job 
        # number since that's the only value required to clear the print queue using the lprm command.
        if round(two_hours_diff.seconds/60/60) > 2:
          queue_remove_command = 'lprm %s' %key.split('-', 1)[-1] # this splits the key at '-' and grabs the value after the dash which 
                                                                  # is the print job number.
          queue_remove_proc = subprocess.Popen(queue_remove_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
          
        else:
          pass      
