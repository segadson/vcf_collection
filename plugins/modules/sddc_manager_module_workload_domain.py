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

def main():
    parameters = dict(
    sddc_manager_ip=dict(type='str', required=True),
    sddc_manager_user=dict(type='str', required=True),
    sddc_manager_password=dict(type='str', required=True, no_log=True),
    state=dict(type='str', choices=['create', 'delete', 'validate'], required=True),
    workload_domain_payload=dict(type='dict', required=True),
)

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    workload_domain_payload = module.params['workload_domain_payload']
    state = module.params['state']

    if state == 'validate':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_domains(workload_domain_payload)
            print(api_response)
            payload_data = api_response["data"]
            module.exit_json(changed=False, meta=payload_data)
        except Exception as e:
            module.fail_json(msg="Failed to validate workload domain: " + str(e))
    elif state == 'create':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.create_domains(workload_domain_payload)
            payload_data = api_response["data"]
            module.exit_json(changed=False, meta=payload_data)
        except:
            module.fail_json(msg="Failed to create workload domain")
    elif state == 'update':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.update_domains(workload_domain_payload)
            payload_data = api_response["data"]
            module.exit_json(changed=False, meta=payload_data)
        except:
            module.fail_json(msg="Failed to update workload domain")
    elif state == 'delete':
        '''
        To do:
        - Add Check for any VMs on clusters
        - Check for remote Datastores
        - Auto migrate VMs to other clusters in a different domain? 
        '''
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.delete_domains(workload_domain_payload)
            payload_data = api_response["data"]
            module.exit_json(changed=False, meta=payload_data)
        except:
            module.fail_json(msg="Failed to delete workload domain")
    
if __name__ == '__main__':
    main()

