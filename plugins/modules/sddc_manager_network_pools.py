#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible.module_utils.basic import *
from module_utils.sddc_manager import SddcManagerApiClient
from module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation
def get_network_pool_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, network_pool_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_network_pools()
    network_pools = api_response.data
    for network_pool in network_pools:
        if network_pool['name'] == network_pool_name:
            return network_pool['id']
    return None

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
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    state = module.params['state']
    network_payload = module.params['network_payload']

    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)

    CREATE = 'create'
    DELETE = 'delete'
    UPDATE = 'update'

    # ...existing code...

    state_methods = {
        CREATE: api_client.create_network_pools,
        DELETE: api_client.delete_network_pools,
        UPDATE: api_client.update_network_pools,
    }

    if state in state_methods:
        try:
            network_pool_id = None
            if state != CREATE:
                network_pool_name = module.params['network_pool_name']
                network_pool_obj = get_network_pool_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, network_pool_name)
                if network_pool_obj is None:
                    raise ValueError(f"Network pool with name {network_pool_name} not found")
                network_pool_id = network_pool_obj['id']
            
            api_response = state_methods[state](network_pool_id, network_payload) if network_pool_id else state_methods[state](network_payload)
            if api_response and api_response.data:
                payload_data = api_response.data
                module.exit_json(changed=True, meta=payload_data)
            else:
                raise ValueError("API response is empty")
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")
    else:
        module.fail_json(msg="Error: Invalid State")

    # state_methods = {
    #     'create': api_client.create_network_pools,
    #     'delete': api_client.delete_network_pools,
    #     'update': api_client.update_network_pools,
    # }

    # if state in state_methods:
    #     try:
    #         if state == 'create':
    #             api_response = state_methods[state](network_payload)
    #         else:
    #             network_pool_name = module.params['network_pool_name']
    #             network_pool_obj = get_network_pool_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, network_pool_name)
    #             if network_pool_obj is None:
    #                 raise ValueError(f"Network pool with name {network_pool_name} not found")
    #             network_pool_id = network_pool_obj['id']
    #             api_response = state_methods[state](network_pool_id, network_payload)
    #         payload_data = api_response.data
    #         module.exit_json(changed=True, meta=payload_data)
    #     except VcfAPIException as e:
    #         module.fail_json(msg=f"Error: {e}")
    # else:
    #     module.fail_json(msg="Error: Invalid State")
    
    ################################################
    # Maybe add ip pools    sddc_manager_ip = module.params['sddc_manager_ip']
    ################################################

if __name__ == '__main__':
    main()