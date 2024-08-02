import os
import sys


# current_dir = os.path.dirname(os.path.realpath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

import requests
import requests.packages
import json
from json import JSONDecodeError
import logging
from typing import List, Dict
from ansible_collections.vmware.vcf.plugins.moduleutils.exceptions import VcfAPIException
from ansible_collections.vmware.vcf.plugins.moduleutils.outputs import Result

class VsphereApiWrapper:
    def __init__(self, vcenter_host: str, vcenter_username: str, vcenter_password: str):
        self.vcenter_host = vcenter_host
        self.session = requests.Session()
        self.session.verify = False

        try:
            url = f"https://{vcenter_host}/rest/com/vmware/cis/session"
            response = self.session.post(url, auth=(vcenter_username, vcenter_password))
            response.raise_for_status()
            self.session.headers.update({'vmware-api-session-id': response.json()['value']})
        except requests.exceptions.RequestException as e:
            raise VcfAPIException(f"Failed to obtain session token: {str(e)}")
        except (KeyError, JSONDecodeError) as e:
            raise VcfAPIException(f"Failed to parse session token response: {str(e)}")

    def _make_request(self, method: str, url: str) -> Result:
        try:
            response = self.session.request(method, url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise VcfAPIException(f"Failed to make {method} request to {url}: {str(e)}")
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            raise VcfAPIException("Bad JSON in response") from e
        is_success = 299 >= response.status_code >= 200
        if is_success:
            return Result(response.status_code, message=response.reason, data=data_out)

        raise VcfAPIException(f"{response.status_code}: {response.reason}")

    def get_all_clusters(self) -> Result:
        url = f"https://{self.vcenter_host}/rest/vcenter/cluster"
        return self._make_request('GET', url)
    
    def get_host_desired_image(self, host_id: str) -> Result:
            url = f"https://{self.vcenter_host}/rest/vcenter/lcm/host/{host_id}/desired-image"
            return self._make_request('GET', url)
    def create_cluster(self, datacenter_id: str, cluster_spec: dict) -> Result:
        '''
        cluster_spec = {
            "spec": {
                "name": "your-cluster-name",
                "datacenter": datacenter_id,
                "drs_enabled": True,
                "ha_enabled": True
            }
        }
        '''
        url = f"https://{self.vcenter_host}/rest/vcenter/cluster"
        return self._make_request('POST', url, data=cluster_spec)
    
    def assign_cluster_desired_image(self, cluster_id: str, image_spec: dict) -> Result:
        '''
        image_spec = {
            "spec": {
                "image": "your-image-name"
            }
        } 
        '''
        url = f"https://{self.vcenter_host}/rest/vcenter/lcm/cluster/{cluster_id}/desired-image"
        return self._make_request('POST', url, data=image_spec)