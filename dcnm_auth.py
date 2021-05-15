#!/usr/bin/python
def auth(url, dcnm_user, dcnm_pass):
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    from requests.auth import HTTPBasicAuth
    import json

    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+' \
                                                          'AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+' \
                                                          '3DES:!aNULL:!MD5:!DSS'

    response = requests.post(url + '/rest/logon',
                             data=json.dumps({'expirationTime': 999999}),
                             auth=HTTPBasicAuth(dcnm_user, dcnm_pass),
                             verify=False
                             )

    dcnm_token = json.loads(response.text)['Dcnm-Token']

    return dcnm_token
