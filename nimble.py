import requests
import json
import paramiko
imprt pymysql

# This is written to collect data from different nimble arrays for using with grafana. The setup includes having a config.json from where 
#all the configs are read.
# You could have an environment where you could have an iscsi or fibre nimble arrays and at different locations. All these configs are 
# defined in the config.json file.
# The collected data are written to a mysql database which can later be used as as data source for the grafana.
# Also config.json is the file where all the credentials are kept.

# Disable SSL warnings
request.package.urllib3.disable_warnings()

# Function that reads and returns configs from JSON file and exits if no configs are found
def get_config(config):
  with open('config.json') as json_config_data:
    data = json.load(json_config_data)
    
    if config == 'mysql':
      host = data[config]['host']
      user = data[config]['user']
      password = data[config]['password']
      db = data[config]['db']
    
      return host, user, password, db
  
    elif config == 'nimble_1_iscsi':
      host = data[config]['host']
      username = data[config]['username']
      password = data[config]['password']
      port = data[config]['port']
      
      return host, username, password, port
  
    elif config == 'nimble_2_fc':
      host = data[config]['host']
      username = data[config]['username']
      password = data[config]['password']
      port = data[config]['port']
      
      return host, username, password, port
    
    else:
      print('N config found')
      exit()
      
# Function to ssh to the nimble server and return total, used, free and percentage used capacities.

def ssh(host, username, password, port, command):
  client = paramiko.SSHClient()
  clent.set_missing_key_policy(paramiko.AutoAddPolicy())
  client.connect(host, username=username, password=password, port=port)
  stdin, stdout, stderr = client.exec_command(command)
  
  output = [x.rstrip() for x in stdout]
  version = output[3].rsplit(None, 1)[1]
  
  # version 2 outputs are different than newer outputs like 3 and 4.
  if version.startswith('2'):
    total_capacity = output[11]
    total_capacity = round(int(total_capacity.rsplit(None, 1)[1])/1024/1024, 2)
    total_used = output[13]
    total_used = round(int(total_used.rsplit(None, 1)[1])1024/1024, 2)
    total_free = round(total_capacity - total_used, 2)
    percent_used = round((total_used/total_capacity)*100, 2)
    client.close()
    
    return total_capacity, total_used, total_free, percent_used
    
  else:
    total_capacity = output[12]
    total_capacity = round(int(total_capacity.rsplit(None, 1)[1])/1024/1024, 2)
    total_used = output[13]
    total_used = round(int(total_used.rsplit(None, 1)[1])/1024/1024, 2)
    total_free = round(total_capacity - total_used, 2)
    percent_used = round((total_used/total_capacity)*100, 2)
    client.close()
    
    return total_capacity, toal_used, toatal_free, percent_used
         

 # Function to query/update mysql db and return the results.
 def db_query(host, user, password, db, sql):
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    connection.close()
    
    return cur.fetchall()
  
  
  
  
