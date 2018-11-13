# List all the vms from ovm manager using the REST API. 
# Print the list in a nice table format using prettytable.
import requests
import json
from prettytable import PrettyTable

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

url = 'https://ovm-manager-url:7002/ovm/core/wsapi/rest'
vm_endpoint = '/Vm/'
username = 'your_username'
password = 'your_password'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

response = requests.get(url + vm_endpoint, auth=(username, password), headers=headers, verify=False)

table = PrettyTable()

# Adding filed names to the table instance that we just created above
table.filed_names = ["VM NAME", "STATE", "MEMORY(GB)", "CPU", "OS", "DOMAIN TYPE", "DESCRIPTION"]

# Adding the data to the table fields.
for i in response.json():
  table.add_row([i['name'], i['vmRunState'], i['memoryLimit']/1024, i['cpuCount'], i['osType'], i['vmDomainType'], i['description']])
  
# Aligning the text in the table to the left
table.align = 'l'
print(table)
