#!/usr/bin/python
import sys
# sys.path.append('/home/segadson/vcf/ansible_vcf/plugins')

from ansible.module_utils.basic import *
from ansible.module_utils.sddc_manager import SddcManagerApiClient
from ansible.module_utils.exceptions import VcfAPIException
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
            print("Element: ", element['fqdn'])
            if element['fqdn'] == hosts_name and element['status'] != 'UNASSIGNED_USEABLE' and element['status'] != 'ASSIGNED':
                print(f"Host {hosts_name} is not Valid")
            else:
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

def get_network_pool_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_network_pools()
    payload_data = api_response.data
    for element in payload_data['elements']:
        if element['name'] == name:
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

    host_list = hosts_list_payload['hosts']

    #Check for vvolStorageProtocolType
    if state == 'commission':
        for item in host_list:
            if item['vvolStorageProtocolType'] == None and item['storageType'] == ['VVOL', 'NFS', 'VMFS_FC']:
                module.fail_json(msg="vvolStorageProtocolType is required for VVOL, NFS or VMFS_FC StorageType")
            elif item['vvolStorageProtocolType'] == None and item['storageType'] == ['VSAN', 'VSAN_ESA', 'VSAN_REMOTE']:
                module.fail_json(msg="vvolStorageProtocolType should be null")

    print("Host List: ", host_list)
    if state == 'commission' and validate == True:
        #############
        # Get Network Pool by Name and add to payload
        ###############
        # updated_host_payload = get_hosts_by_name_valid_for_commisson(sddc_manager_ip, sddc_manager_user, 
        #                                                              sddc_manager_password, host_list)
        
        for item in updated_host_payload:
            item['networkPoolId'] = get_network_pool_by_name(sddc_manager_ip, sddc_manager_user, 
                                                             sddc_manager_password, item['networkPoolName'])['id']

        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_hosts(json.dumps(updated_host_payload))
            payload_data = api_response.data
            module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")
    elif state == 'commission' and validate == False:
        # updated_host_payload = get_hosts_by_name_valid_for_commisson(sddc_manager_ip, sddc_manager_user, 
        #                                                              sddc_manager_password, host_list)
        for item in updated_host_payload:
            item['networkPoolId'] = get_network_pool_by_name(sddc_manager_ip, sddc_manager_user, 
                                                             sddc_manager_password, item['networkPoolName'])['id']
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.commission_hosts(json.dumps(updated_host_payload))
            payload_data = api_response.data
            module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")
    elif state == 'decommission' and validate == False:

        updated_host_payload = get_hosts_by_name_valid_for_decommisson(sddc_manager_ip, sddc_manager_user, 
                                                                     sddc_manager_password, host_list)
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.decommission_hosts(json.dumps(updated_host_payload))
            payload_data = api_response.data
            module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")
    else:
        module.exit_json(changed=False, meta="Not Valid Action")

if __name__ == '__main__':
    main()    