#!/usr/bin/python
import sys
# sys.path.append('/home/segadson/vcf/ansible_vcf/plugins')

from ansible_collections.vmware.vcf.plugins.moduleutils.basic import *
from ansible_collections.vmware.vcf.plugins.moduleutils.sddc_manager import SddcManagerApiClient
from ansible_collections.vmware.vcf.plugins.moduleutils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation
DOCUMENTATION = '''
---
module: sddc_manager_host_commisson
short_description: This module manages the commissioning and decommissioning of hosts in SDDC Manager
description:
    - "This module is a wrapper around the SDDC Manager hosts API. It allows to commission and decommission hosts."
author:
    - Your Name (@yourusername)
options:
    sddc_manager_ip:
        description:
            - The IP address of the SDDC Manager.
        required: true
        type: str
    sddc_manager_user:
        description:
            - The username for the SDDC Manager.
        required: true
        type: str
    sddc_manager_password:
        description:
            - The password for the SDDC Manager.
        required: true
        type: str
    hosts_list_payload:
        description:
            - The list of hosts to be commissioned or decommissioned.
        required: true
        type: list
    state:
        description:
            - The state of the hosts. Choices are 'commission', 'decommission'.
        required: true
        type: str
requirements:
    - python >= 3.6
'''

EXAMPLES = '''
# How to use this module in your playbook
- name: Commission hosts
  sddc_manager_host_commisson:
    sddc_manager_ip: "192.168.1.1"
    sddc_manager_user: "admin"
    sddc_manager_password: "password"
    hosts_list_payload: ["host1", "host2"]
    state: "commission"
'''

RETURN = '''
hosts:
    description: The hosts that were commissioned or decommissioned.
    returned: always
    type: list
'''

'''
Commisson Host:
1) Check if host are in inventory
    - If not, commission free for commission 
    - Validate Host
    - If Pass then Commission host

2) Decommission Host:
    - Check if host are in inventory with UNASSIGNED_USEABLE
'''
class SddcManagerHostCommission:
    def __init__(self, module):
        self.module = module
        self.sddc_manager_ip = module.params['sddc_manager_ip']
        self.sddc_manager_user = module.params['sddc_manager_user']
        self.sddc_manager_password = module.params['sddc_manager_password']
        self.hosts_list_payload = module.params['hosts_list_payload']
        self.api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)

    def get_hosts_by_name_valid_for_commisson(self):
        hosts_list_payload = self.hosts_list_payload
        valid_hosts_lists = []
        for host in hosts_list_payload:
            hosts_name = host['fqdn']
            api_response = self.api_client.get_all_hosts()
            payload_data = api_response.data
            for element in payload_data['elements']:
                if element['fqdn'] == hosts_name and element['status'] != 'UNASSIGNED_USEABLE' and element['status'] != 'ASSIGNED':
                    print(f"Host {hosts_name} is not Valid")
                else:
                    valid_hosts_lists.append(host)
        return valid_hosts_lists
    
    def get_hosts_by_name_valid_for_decommisson(self):
        hosts_list_payload = self.hosts_list_payload
        valid_hosts_lists = []
        for host in hosts_list_payload:
            hosts_name = host['fqdn']
            api_response = self.api_client.get_all_hosts()
            payload_data = api_response.data
            for element in payload_data['elements']:
                if element['fqdn'] == hosts_name and element['status'] == 'UNASSIGNED_USEABLE':
                    valid_hosts_lists.append(hosts_name)
        return valid_hosts_lists
    
    def get_network_pool_by_name(self, name):
        api_response = self.api_client.get_network_pools()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == name:
                return element
        return None

    def host_commission_validate_hosts(self):
        hosts_list_payload = self.hosts_list_payload
        updated_host_payload = hosts_list_payload['hosts']
        for item in updated_host_payload:
            item['networkPoolId'] = self.get_network_pool_by_name(item['networkPoolName'])['id']
        try:
            api_response = self.api_client.validate_hosts(json.dumps(updated_host_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def host_commission_commission_hosts(self):
        hosts_list_payload = self.hosts_list_payload
        updated_host_payload = hosts_list_payload['hosts']
        for item in updated_host_payload:
            item['networkPoolId'] = self.get_network_pool_by_name(item['networkPoolName'])['id']
        try:
            api_response = self.api_client.commission_hosts(json.dumps(updated_host_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")
    
    def host_commission_decommission_hosts(self):
        hosts_list_payload = self.hosts_list_payload
        updated_host_payload = hosts_list_payload['hosts']
        updated_host_payload = self.get_hosts_by_name_valid_for_decommisson()
        try:
            api_response = self.api_client.decommission_hosts(json.dumps(updated_host_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def run(self):
        if self.module.params['state'] == 'commission' and self.module.params['validate'] == True:
            result = self.host_commission_validate_hosts()
            self.module.exit_json(changed=False, meta=result)
        elif self.module.params['state'] == 'commission' and self.module.params['validate'] == False:
            result = self.host_commission_commission_hosts()
            self.module.exit_json(changed=True, meta=result)
        elif self.module.params['state'] == 'decommission' and self.module.params['validate'] == False:
            result = self.host_commission_decommission_hosts()
            self.module.exit_json(changed=True, meta=result)            
        else:
            self.module.fail_json(msg="Not Valid Action")

def main():
    parameters = dict(
        sddc_manager_ip=dict(required=True, type='str'),
        sddc_manager_user=dict(required=True, type='str'),
        sddc_manager_password=dict(required=True, type='str'),
        hosts_list_payload=dict(required=True, type='dict'),
        validate=dict(required=False, type='bool', default=False),
        state=dict(required=True, type='str', choices=['commission', 'decommission'])
    )

    module = AnsibleModule(argument_spec=parameters, supports_check_mode=True)
    host_commission = SddcManagerHostCommission(module)
    host_commission.run()

if __name__ == '__main__':
    main()