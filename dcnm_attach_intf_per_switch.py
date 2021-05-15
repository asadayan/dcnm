#!/usr/bin/python
# Author Ahamed Sadayan

import dcnm_auth
import json
import requests
import dcnm_credentials
import dcnm_modules
import sys
import re
import pprint


if len(sys.argv) < 4:
    print(f'usage python {sys.argv[0]} fabric-name intf_range network_prefix switch_name')
    print('Example python dcnm_attach_intf e1/1,e1/5|e1/1-3 ibm all')
    sys.exit()
fabricName = sys.argv[1]
intf_range = sys.argv[2]
network_prefix = sys.argv[3]
switchName = sys.argv[4]
if len(sys.argv) == 5:
    fetch = 'all'
else:
    fetch = 'undeployed'

interface = ''
port_range =   re.findall('[Eethrnt](\d+)/(\d+)-(\d+)',intf_range)
if len(port_range) != 0:
    for item in port_range:
        for port in range(int(item[1]),int(item[2])+1):
            interface += f'Ethernet{item[0]}/{port},'

port =   re.findall('[Eethrnt](\d+)/(\d+(,|$))',intf_range)
if len(port) != 0:
    for item in port:
        interface += f'Ethernet{item[0]}/{item[1]}'

port_range =  re.findall('po(\d+)-(\d+)',intf_range)
if len(port_range) != 0:
    for item in port_range:
        for port in range(int(item[0]), int(item[1]) + 1):
            interface += f'Port-channel{port},'


port = re.findall('po(\d+)(,|$)',intf_range)
if len(port) != 0:
    for item in port:
        interface += f'Port-channel{item[0]},'



# port_range =  re.findall('vpc(\d+)-(\d+)',intf_range)
# if len(port_range) != 0:
#     for item in port_range:
#         for port in range(int(item[0]), int(item[1]) + 1):
#             interface += f'vPC{port},'
#
#
# port = re.findall('vpc(\d+)(,|$)',intf_range)
# if len(port) != 0:
#     for item in port:
#         interface += f'vPC{item[0]},'
#
# if interface[-1] == ',':
#     interface = interface[:-1]


print(interface)


username = dcnm_credentials.username
password = dcnm_credentials.password
url = 'https://' + dcnm_credentials.node_ip
posturl = url + f'/rest/top-down/fabrics/{fabricName}/networks/attachments'
dcnm_token = dcnm_auth.auth(url,username,password)
headers = {'Dcnm-Token': dcnm_token, 'Content-Type': 'application/json'}
leaf_nodes = dcnm_modules.get_leaf_nodes(fabricName)
network_list = dcnm_modules.network_list(fabricName,fetch)
#print(network_list)
#sys.exit()
payload_list = []
lanattachedlist = []
for node in leaf_nodes:
    if node['name'] == switchName:
        for network in network_list:
            if network['network'].lower()[:3] == network_prefix.lower():
                if node['vpc_peer'] == None:
                    lanattach = {
                        "fabric": fabricName,
                        "networkName": network['network'],
                        "serialNumber": node['serial_no'],
                        "switchPorts": str(interface),
                        "detachSwitchPorts": "",
                        "vlan": network['vlan'],
                        "dot1QVlan": 1,
                        "untagged": False,
                        "freeformConfig": "",
                        "deployment": True,
                        "extensionValues": "",
                        "instanceValues": ""
                    }
                    lanattachedlist.append(lanattach)
                else:
                    peer_serial_no = dcnm_modules.get_serial_num(leaf_nodes,node['vpc_peer'])
                    lanattach = {
                        "fabric": fabricName,
                        "networkName": network['network'],
                        "serialNumber": node['serial_no'],
                        "switchPorts": str(interface),
                        "detachSwitchPorts": "",
                        "vlan": network['vlan'],
                        "dot1QVlan": 1,
                        "untagged": False,
                        "freeformConfig": "",
                        "deployment": True,
                        "extensionValues": "",
                        "instanceValues": ""
                    }
                    lanattachedlist.append(lanattach)
                    lanattach = {
                        "fabric": fabricName,
                        "networkName": network['network'],
                        "serialNumber": peer_serial_no,
                        "switchPorts": "",
                        "detachSwitchPorts": "",
                        "vlan": network['vlan'],
                        "dot1QVlan": 1,
                        "untagged": False,
                        "freeformConfig": "",
                        "deployment": True,
                        "extensionValues": "",
                        "instanceValues": ""
                    }
                    lanattachedlist.append(lanattach)
                    lanattach = {}
                payload =   {
                        "networkName": network['network']
                        }
                payload["lanAttachList"] = lanattachedlist
                payload_list.append(payload)
                payload = {}
                lanattachedlist = []
            else:
                print(f"Network name prefix not matching skipping network {network['network']}")

# pprint.pprint(payload_list)
# sys.exit()
    response = requests.post(posturl,
                             data=json.dumps(payload_list),
                             verify=False,
                             headers=headers)


    if response.status_code == 200:
        output = json.loads(response.text)
        print(f"attached interfaces to node {node['name']},{node['mgmt_ip']}")
        pprint.pprint(output)
    else:
        output = response.reason
        print(f" Error attaching interfaces to node {node['name']},{node['mgmt_ip']},{output}")
    #pprint.pprint(payload_list)
    payload_list = []


save = input('Do you want to save and deploy?[Y/N]')

if save.lower() == 'y' or save.lower() == 'yes':
    output = dcnm_modules.save_config(fabricName)
    print(output)

    output = dcnm_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')

