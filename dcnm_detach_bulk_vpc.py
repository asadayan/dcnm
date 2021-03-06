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

def is_net_in_intf(port_chnl_list,netWork):
    for item in port_chnl_list:
        if netWork in item['attached_net']:
            return True
    return False

if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name [net-prefix]')
    sys.exit()

fabricName = sys.argv[1]
if len(sys.argv) == 3:
    netPrefix = str(sys.argv[2])

username = dcnm_credentials.username
password = dcnm_credentials.password
url = 'https://' + dcnm_credentials.node_ip
dcnm_token = dcnm_auth.auth(url,username,password)
headers = {'Dcnm-Token': dcnm_token, 'Content-Type': 'application/json'}
po_list = dcnm_modules.get_vpc_nodes(fabricName)
net_list = dcnm_modules.network_list(fabricName,'all')
port_chnl_list = dcnm_modules.get_port_channels(fabricName)
network_list = []
for net in net_list:
    if net['network'][:3].lower() == netPrefix[:3].lower():
        network_list.append(net)

#print(network_list)
#sys.exit()
node_names =''

for net in network_list:
    attach=[]
    if is_net_in_intf(port_chnl_list,net['network']):
        for node in po_list:
            pair1 = {
                    "fabric": fabricName,
                    "networkName": net["network"],
                    "serialNumber":node["serial_no"],
                    "switchPorts": "",
                    "detachSwitchPorts": "",
                    "vlan": net['vlan'],
                    "dot1QVlan": 1,
                    "untagged": False,
                    "freeformConfig": "",
                    "deployment": False,
                    "extensionValues": "",
                    "instanceValues": ""
                }
            pair2 = {
                    "fabric": fabricName,
                    "networkName": net["network"],
                    "serialNumber": node["peer_serial_no"],
                    "switchPorts": "",
                    "detachSwitchPorts": "",
                    "vlan": net['vlan'],
                    "dot1QVlan": 1,
                    "untagged": False,
                    "freeformConfig": "",
                    "deployment": False,
                    "extensionValues": "",
                    "instanceValues": ""
                }
            attach.append(pair1)
            attach.append(pair2)
        detach_load = [{
            "networkName": net['network'],
            "lanAttachList":attach}]
        posturl = url + f'/rest/top-down/fabrics/{fabricName}/networks/attachments'
        response = requests.post(posturl, data=json.dumps(detach_load), verify=False, headers=headers)
        reason = response.reason
        if response.status_code == 200:
            output = response.text
            print(f"Detached interface from vpc nodes for the network {net['network']}, nodes {node['name']}--{node['nname']}")
        elif reason.strip() == 'Unauthorized':
            dcnm_token = dcnm_auth.auth(url, username, password)
            headers = {'Dcnm-Token': dcnm_token, 'Content-Type': 'application/json'}
            posturl = url + f'/rest/top-down/fabrics/{fabricName}/networks/attachments'
            response = requests.post(posturl, data=json.dumps(detach_load), verify=False, headers=headers)
            output = response.text
            print(f"Detached interface from vpc nodes for the network {net['network']} nodes {node['name']}--{node['nname']}")
        else:
            print('Error:', response.reason)
    else:
        print(f"No interface in {net['network']} - skipping")





save = input('Do you want to save and deploy?[Y/N]: ')

if save.lower() == 'y' or save.lower() == 'yes':
    output = dcnm_modules.save_config(fabricName)
    print(output)

    output = dcnm_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')

