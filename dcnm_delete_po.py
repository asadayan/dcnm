#!/usr/bin/python
# Author Ahamed Sadayan

import dcnm_auth
import json
import requests
import dcnm_credentials
import sys
import dcnm_modules
import pprint
import re

if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name ')
    sys.exit()

fabricName = sys.argv[1]


username = dcnm_credentials.username
password = dcnm_credentials.password
url = 'https://' + dcnm_credentials.node_ip
dcnm_token = dcnm_auth.auth(url,username,password)
headers = {'Dcnm-Token': dcnm_token, 'Content-Type': 'application/json'}
po_list = dcnm_modules.get_port_channels(fabricName)
#pprint.pprint(po_list)
payload_list =[]
for item in po_list:
    if  len(item['attached_net']) == 0 and int(item['vpc_id']) == 0:
        serialNum = item['serial_no']
        payload =[{
                'ifName': item['po_name'],
                'serialNumber': serialNum
            }]
        payload_list.append(json.dumps(payload))




posturl = url + '/rest/interface/markdelete'
for load in payload_list:
    response = requests.delete(posturl, data=load, verify=False, headers=headers)
    if response.status_code == 200:
        output = response.text
        pprint.pprint(f'Marked for deletion {load.strip()}')
    #else:
    #    print(f'Error deleting {load}',response.reason)

posturl = url + '/rest/globalInterface/deploy'
for load in payload_list:
    response = requests.post(posturl, data=load, verify=False, headers=headers)
    if response.status_code == 200:
        output = response.text
        pprint.pprint(f'Deletion Deployed {load}')
    else:
        print(f'Error deploying {load}',response.reason)


save = input('Do you want to save and deploy?[Y/N]: ')

if save.lower() == 'y' or save.lower() == 'yes':
    output = dcnm_modules.save_config(fabricName)
    print(output)

    output = dcnm_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')



