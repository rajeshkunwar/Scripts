# 

import requests
import json
import datetime

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

url = 'https://nimble:5392/v1'
username = 'your_username'
password = 'your_password'
date_time = datetime.datetime.today().strftime('%m-%d-%y-%H:%M:%S')

def get_token()
  token_endpoint = '/tokens'
  data = {'data': {'username': username, 'password': password}}
  
  response = requests.post(url + token_endpoint, data = json.dumps(data), verify=False)
  if response.status_code == 201:
    


import functools

def get_id(func):
  
  @functools.wraprs(func)
  
  def wrapper_get_id(*args, **kwargs):
    token = get_token()
    headers = {'X-Auth-Token': token}




@decorator
def decorated_func():
  response = requests.post
