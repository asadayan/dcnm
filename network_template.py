#!/usr/bin/python
# Author Ahamed Sadayan
# Template for http post Netowrk creation
# After import make changes to the releavent field



network = {'displayName': 'MyNetwork_30000',
 'fabric': 'IBM_VxLAN_Fabric',
 'networkExtensionTemplate': 'Default_Network_Extension_Universal',
 'networkId': '30000',
 'networkName': 'MyNetwork_30000',
 'networkTemplate': 'Default_Network_Universal',
 'networkTemplateConfig': {'dhcpServerAddr1': '',
                           'dhcpServerAddr2': '',
                           'enableIR': False,
                           'enableL3OnBorder': True,
                           'gatewayIpAddress': '10.1.1.1/24',
                           'gatewayIpV6Address': '2001::1/64',
                           'intfDescription': '',
                           'isLayer2Only': False,
                           'loopbackId': '',
                           'mcastGroup': '239.1.1.0',
                           'mtu': '',
                           'networkName': 'MyNetwork_30000',
                           'nveId': 1,
                           'rtBothAuto': True,
                           'secondaryGW1': '',
                           'secondaryGW2': '',
                           'segmentId': '30000',
                           'suppressArp': True,
                           'tag': '12345',
                           'trmEnabled': False,
                           'vlanId': '',
                           'vlanName': '',
                           'vrfDhcp': '',
                           'vrfName': 'Customer-001'},
 'serviceNetworkTemplate': None,
 'source': None,
 'vrf': 'Customer-001'}