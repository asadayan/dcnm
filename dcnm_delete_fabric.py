#!/usr/bin/python
# Author Ahamed Sadayan

import dcnm_auth
import json
import requests
import dcnm_credentials
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name ')
    sys.exit()
fabricName = sys.argv[1]
username = dcnm_credentials.username
password = dcnm_credentials.password
url = 'https://' + dcnm_credentials.node_ip
posturl = url + f'/rest/control/fabrics/{fabricName}'
dcnm_token = dcnm_auth.auth(url,username,password)
headers = {'Dcnm-Token': dcnm_token, 'Content-Type': 'application/json'}
deleteurl = url + '/rest/control/fabrics/' + fabricName
payload = {"sync": "true", "query": {}}
response = requests.delete(deleteurl,
                           data=json.dumps(payload),
                           headers=headers,
                           verify=False)
print(response.text)