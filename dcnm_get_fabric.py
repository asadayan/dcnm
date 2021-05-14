#!/usr/bin/python
# Author Ahamed Sadayan

import dcnm_auth
import json
import requests
import dcnm_credentials
import sys
import pprint


if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name')
    sys.exit()
fabricName = sys.argv[1]

username = dcnm_credentials.username
password = dcnm_credentials.password
url = 'https://' + dcnm_credentials.node_ip
posturl = url + f'/rest/control/fabrics/{fabricName}'
dcnm_token = dcnm_auth.auth(url,username,password)
headers = {'Dcnm-Token': dcnm_token, 'Content-Type': 'application/json'}


response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)

pprint.pprint(output)
