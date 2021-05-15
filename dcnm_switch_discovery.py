#!/usr/bin/python
# Author Ahamed Sadayan

import dcnm_auth
import json
import requests
import dcnm_credentials
import sys
import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if len(sys.argv) < 3:
    print(f'usage python {sys.argv[0]} fabric-name  seed_ip')
    print('example: python dcnm_discovery.py test-fabric 172.13.1.2')
    sys.exit()
fabricName = sys.argv[1]
seedIP = sys.argv[2]
username = dcnm_credentials.username
password = dcnm_credentials.password
sw_username = dcnm_credentials.sw_username
sw_password = dcnm_credentials.sw_password
maxHops = 2

url = 'https://' + dcnm_credentials.node_ip
posturl = url + f'/rest/control/fabrics/{fabricName}'
dcnm_token = dcnm_auth.auth(url,username,password)
headers = {'Dcnm-Token': dcnm_token, 'Content-Type': 'application/json'}
response = requests.get(posturl, verify=False, headers=headers)
fabric = json.loads(response.text)
fabric_id = fabric['id']
if fabric_id == -1:
    print('Invalid Fabric ID found')
    sys.exit()

# to post dcnm data with the seed ip #
posturl = url + f'/rest/control/fabrics/{fabric_id}/inventory/test-reachability'
print(posturl)
payload =  {
    "seedIP": seedIP,
    "snmpV3AuthProtocol": "0",
    "username": sw_username,
    "password": sw_password,
    "maxHops": maxHops,
    "cdpSecondTimeout": "5",
    "preserveConfig": "false",
    "platform": "null"
}
response = requests.post(posturl,
                         data=json.dumps(payload),
                         headers=headers,
                         verify=False)


# add switch from the list of switches got from the response
data = json.loads(response.text)
#pprint.pprint(response.text)
switches =[]

for item in data:
    #print(f'>>>{item}')
    #sys.exit()
    switches.append(dict(deviceIndex = item["deviceIndex"],
                         sysName = item["sysName"],
                         platform = item["platform"],
                         version = item["version"],
                         ipaddr= item["ipaddr"]))

payload = {"switches": switches,
           "seedIP": seedIP,
           "username": sw_username,
           "password": sw_password,
           "preserveConfig":"false"
           }


posturl = url + f'/rest/control/fabrics/{fabric_id}/inventory/discover'
response = requests.post(posturl,
                         data=json.dumps(payload),
                         headers=headers,
                         verify=False)

pprint.pprint(response.text)
