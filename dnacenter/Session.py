#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth

try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
except ImportError:
    pass


headers = {'Content-type': 'Application/json',
           'Accept': 'Application/json'}

class Session(object):
    def __init__(self, username, dnacenter, auth_header, ssl_verify):

        self.username = username
        self.dnacenter = dnacenter
        self.token = auth_header
        self.headers = auth_header
        self.ssl_verify = ssl_verify

    @classmethod
    def login(cls, username, password, dnacenter, ssl_verify=False):
        r = None

        headers = {'Content-type': 'Application/json',
                   'Accept': 'Application/json'}

        if not ssl_verify:
            try:
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            except AttributeError:
                pass
        r = requests.post(
            url='https://' + dnacenter + '/api/system/v1/auth/token',
            headers=headers,
            verify=ssl_verify,
            auth=HTTPBasicAuth(username, password))

        auth_header = {'Content-type': 'Application/json',
                       'Accept': 'Application/json',
                       'X-Auth-Token': r.json()["Token"]}
        # print(r.content)
        return cls(username, dnacenter, auth_header, ssl_verify)



    def _request(self, url, request_method='GET', payload=None, **kwargs):

        url = url

        if request_method == "PUT" or "POST" and payload:
            if type(payload) == dict:
                payload = json.dumps(payload)

            r = requests.request(request_method,
                                 url=url,
                                 headers=self.headers,
                                 verify=self.ssl_verify,
                                 data=payload)

            if not r.ok:
                raise requests.exceptions.HTTPError('HTTP error. Status code was:', r.status_code, r.content)

            return r.content

        elif request_method == "GET":
            r = requests.request(request_method,
                                 url=url,
                                 headers=self.headers,
                                 verify=self.ssl_verify)

            if not r.ok:
                raise requests.exceptions.HTTPError('HTTP error. Status and content:', r.status_code, r.content)

            return json.loads(r.content)

        elif request_method == "DELETE":
            r = requests.request(request_method,
                                 url=url,
                                 headers=self.headers,
                                 verify=self.ssl_verify)

            if not r.ok:
                raise requests.exceptions.HTTPError('HTTP error. Status code was:', r.status_code)

            return r.content


    def get_devices(self):
        return self._request(url=f"https://{self.dnacenter}/api/v1/network-device")

    def get_device_by_id(self, dev_id):
        return self._request(url=f"https://{self.dnacenter}/api/v1/host/{dev_id}/location")

    def get_device_locations(self):
        return self._request(url=f"https://{self.dnacenter}/api/v1//network-device/location")

# "host/"+id+"/location"
# network-device/{id}/location
#
# devices = requests.request(method="GET",
#                            url="https://sandboxdnac.cisco.com/api/v1/network-device",
#                            headers=new_headers,
#                            verify=False)


dna_center = Session.login(username="devnetuser", password="Cisco123!", dnacenter="sandboxdnac.cisco.com")
# print(dna_center.get_devices())
# print(dna_center.dnacenter)
# print(dna_center.get_devices())
print(dna_center.get_device_locations())
# print(dna_center.get_device_by_id(dev_id="d5bbb4a9-a14d-4347-9546-89286e9f30d4"))

# "https://sandboxdnac.cisco.com/api/v1/network-device"

"""
https://sandboxdnac.cisco.com/api/system/v1/auth/login

Username: devnetuser
Password: Cisco123!



https://IP-address/api/v1/network-device

"""