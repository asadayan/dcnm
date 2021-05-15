#!/usr/bin/python
# Author Ahamed Sadayan

import dcnm_auth
import json
import requests
import dcnm_credentials

username = dcnm_credentials.username
password = dcnm_credentials.password
url = 'https://' + dcnm_credentials.node_ip
posturl = url + '/rest/control/fabrics/msd/fabric-associations'
dcnm_token = dcnm_auth.auth(url,username,password)
headers = {'Dcnm-Token': dcnm_token, 'Content-Type': 'application/json'}


response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)


for item in output:
    print(f'Fabric Name: {item["fabricName"]} \tFabric Type: {item["fabricTechnology"]}')

