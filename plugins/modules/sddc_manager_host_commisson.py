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

'''
Commisson Host:
1) Check if host are in inventory
    - If not, commission free for commission 
    - Validate Host
    - If Pass then Commission host

2) Decommission Host:
    - Check if host are in inventory with UNASSIGNED_USEABLE
'''
def get_hosts_by_name_valid_for_commisson(sddc_manager_ip, sddc_manager_user, sddc_manager_password, hosts_list_payload):
    valid_hosts_lists = []
    for host in hosts_list_payload:
        hosts_name = host['fqdn']
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        api_response = api_client.get_all_hosts()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['fqdn'] == hosts_name and element['status'] != 'UNASSIGNED_USEABLE' or element['status'] != 'ASSIGNED':
                valid_hosts_lists.append(host)
    return valid_hosts_lists

def get_hosts_by_name_valid_for_decommisson(sddc_manager_ip, sddc_manager_user, sddc_manager_password, hosts_list_payload):
    valid_hosts_lists = []
    for host in hosts_list_payload:
        hosts_name = host['fqdn']
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        api_response = api_client.get_all_hosts()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['fqdn'] == hosts_name and element['status'] == 'UNASSIGNED_USEABLE':
                valid_hosts_lists.append(hosts_name)
    return valid_hosts_lists

def get_network_pool_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, network_pool_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_network_pools()
    payload_data = api_response.data
    for element in payload_data['elements']:
        if element['name'] == network_pool_name:
            return element
    return None

def main():
    parameters = {
        "sddc_manager_ip": {"required": True, "type": "str"},
        "sddc_manager_user": {"required": True, "type": "str"},
        "sddc_manager_password": {"required": True, "type": "str"},
        "hosts_list_payload": {"required": True, "type": "dict"}, # List of Hosts
        "validate": {"required": False, "type": "bool", "default": False},
        "state": {"required": True, "type": "str", "choices": ['commission', 'decommission']}
    }

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    hosts_list_payload = module.params['hosts_list_payload']
    validate = module.params['validate']
    state = module.params['state']
    
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)

    state_methods = {
        ('validate', True): api_client.validate_hosts,
        ('commission', False): api_client.commission_hosts,
        ('decommission', False): api_client.decommission_hosts,
    }

    get_hosts_methods = {
        'validate': get_hosts_by_name_valid_for_commisson,
        'commission': get_hosts_by_name_valid_for_commisson,
        'decommission': get_hosts_by_name_valid_for_decommisson,
    }

    if (state, validate) in state_methods:
        updated_host_payload = get_hosts_methods[state](sddc_manager_ip, sddc_manager_user, sddc_manager_password, hosts_list_payload)
        for item in updated_host_payload:
            item['networkPoolId'] = get_network_pool_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, item['network_pool_name'])['id']
        try:
            api_response = state_methods[(state, validate)](json.dumps(updated_host_payload))
            payload_data = api_response.data
            module.exit_json(changed=True, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")
    else:
        module.exit_json(changed=False, meta="Not Valid Action")

if __name__ == '__main__':
    main()
