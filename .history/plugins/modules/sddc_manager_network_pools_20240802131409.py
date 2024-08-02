#!/usr/bin/python
import sys
sys.path.append('/home/segadson/vcf/ansible_vcf/plugins')

from ansible_collections.vmware.vcf.plugins.moduleutils.basic import *
from module_utils.sddc_manager import SddcManagerApiClient
from module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation
# def get_network_pool_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, network_pool_name):
#     api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
#     api_response = api_client.get_network_pools()
#     network_pools = api_response.data
#     for network_pool in network_pools:
#         if network_pool['name'] == network_pool_name:
#             return network_pool['id']
#     return None

# def main():
#     parameters = {
#         "sddc_manager_ip": {"required": True, "type": "str"},
#         "sddc_manager_user": {"required": True, "type": "str"},
#         "sddc_manager_password": {"required": True, "type": "str"},
#         "network_payload": {"required": False, "type": "dict", "default": None},
#         "state": {"required": True, "type": "str", "choices": ['create', 'delete', 'update']}
#     }

#     module = AnsibleModule(supports_check_mode=True,
#                            argument_spec=parameters)
    
#     sddc_manager_ip = module.params['sddc_manager_ip']
#     sddc_manager_user = module.params['sddc_manager_user']
#     sddc_manager_password = module.params['sddc_manager_password']
#     state = module.params['state']
#     network_payload = module.params['network_payload']

#     if state == 'create':
#         try:
#             api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
#             api_response = api_client.create_network_pools(network_payload)
#             payload_data = api_response.data
#             module.exit_json(changed=True, meta=payload_data)
#         except VcfAPIException as e:
#             module.fail_json(msg=f"Error: {e}")
#     elif state == 'delete':
#         network_pool_name = module.params['network_pool_name']
#         network_pool_obj = get_network_pool_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, network_pool_name)
#         if network_pool_obj is None:
#             module.fail_json(msg=f"Network pool with name {network_pool_name} not found")
#         network_pool_id = network_pool_obj['id']
#         try:
#             api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
#             api_response = api_client.delete_network_pools(network_pool_id)
#             payload_data = api_response.data
#             module.exit_json(changed=True, meta=payload_data)
#         except VcfAPIException as e:
#             module.fail_json(msg=f"Error: {e}")
#     elif state == 'update':
#         network_pool_name = module.params['network_pool_name']
#         network_pool_obj = get_network_pool_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, network_pool_name)
#         if network_pool_obj is None:
#             module.fail_json(msg=f"Network pool with name {network_pool_name} not found")
#         network_pool_id = network_pool_obj['id']
#         try:
#             api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
#             api_response = api_client.update_network_pools(network_pool_id, network_payload)
#             payload_data = api_response.data
#             module.exit_json(changed=True, meta=payload_data)
#         except VcfAPIException as e:
#             module.fail_json(msg=f"Error: {e}")

#     ################################################
#     # Maybe add ip pools
#     ################################################
#     else:
#         module.fail_json(msg="Error: Invalid State")

# if __name__ == '__main__':
#     main()


class SddcManagerNetworkPools:
    def __init__(self, module):
        self.module = module
        self.sddc_manager_ip = module.params['sddc_manager_ip']
        self.sddc_manager_user = module.params['sddc_manager_user']
        self.sddc_manager_password = module.params['sddc_manager_password']
        self.network_payload = module.params['network_payload']
        self.state = module.params['state']
        self.api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)

    
    def get_network_pool_id_by_name(self):
        api_response = self.api_client.get_network_pools()
        network_pools = api_response.data
        for network_pool in network_pools:
            if network_pool['name'] == self.network_pool_name:
                return network_pool
        return None

    def network_pools_create(self):
        try:
            api_response = self.api_client.create_network_pools(self.network_payload)
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def network_pools_update(self):
        network_pool = self.get_network_pool_id_by_name()
        if network_pool is None:
            self.module.fail_json(msg=f"Network pool with name {self.network_pool_name} not found")
        network_pool_id = network_pool['id']
        try:
            api_response = self.api_client.update_network_pools(network_pool_id, self.network_payload)
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")
    
    def network_pools_delete(self):
        network_pool = self.get_network_pool_id_by_name()
        if network_pool is None:
            self.module.fail_json(msg=f"Network pool with name {self.network_pool_name} not found")
        network_pool_id = network_pool['id']
        try:
            api_response = self.api_client.delete_network_pools(network_pool_id)
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def run(self):
        if self.state == 'create':
            result = self.network_pools_create()
            self.module.exit_json(changed=True, meta=result)
        elif self.state == 'update':
            result = self.network_pools_update()
            self.module.exit_json(changed=True, meta=result)
        elif self.state == 'delete':
            result = self.network_pools_delete()
            self.module.exit_json(changed=False, meta=result)
        else:
            self.module.fail_json(msg="Error: Invalid State")

def main():
    parameters = {
        "sddc_manager_ip": {"required": True, "type": "str"},
        "sddc_manager_user": {"required": True, "type": "str"},
        "sddc_manager_password": {"required": True, "type": "str"},
        "network_payload": {"required": False, "type": "dict", "default": None},
        "state": {"required": True, "type": "str", "choices": ['create', 'delete', 'update']}
    }

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    network_pools = SddcManagerNetworkPools(module)
    network_pools.run()

if __name__ == '__main__':
    main()