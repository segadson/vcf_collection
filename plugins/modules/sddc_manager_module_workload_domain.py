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
    parameters = {
        "sddc_manager_ip": {"required": True, "type": "str"},
        "sddc_manager_user": {"required": True, "type": "str"},
        "sddc_manager_password": {"required": True, "type": "str"},
        "workload_domain_payload": {"required": True, "type": "str"},
        "validate": {"required": True, "type": "bool", "default": False},
        "state": {"required": True, "type": "str", "choices": ["create", "update", "delete"]}

    }

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    workload_domain_payload = module.params['workload_domain_payload']
    validate = module.params['validate']
    state = module.params['state']

    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)

    state_methods = {
        ('create', True): api_client.validate_domains,
        ('create', False): api_client.create_domains,
        ('update', True): api_client.validate_domains,
        ('update', False): api_client.update_domains,
        ('delete', False): api_client.delete_domains,
    }

    try:
        if (state, validate) in state_methods:
            api_response = state_methods[(state, validate)](workload_domain_payload)
            payload_data = api_response.data
            module.exit_json(changed=True, data=payload_data)
        else:
            raise ValueError(f"Invalid state: {state} with validate: {validate}")
    except Exception as e:
        module.fail_json(msg=f"Failed to {state} workload domain with validate: {validate}. Error: {e}")
    # if validate == True and state == 'create' or state == 'update':
    #     try:
    #         api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    #         api_response = api_client.validate_domains(workload_domain_payload)
    #         payload_data = api_response.data
    #         module.exit_json(changed=True, data=payload_data)
    #     except:
    #         module.fail_json(msg="Failed to validate workload domain")
    # elif validate == False and state == 'create':
    #     try:
    #         api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    #         api_response = api_client.create_domains(workload_domain_payload)
    #         payload_data = api_response.data
    #         module.exit_json(changed=True, data=payload_data)
    #     except:
    #         module.fail_json(msg="Failed to create workload domain")
    # elif validate == False and state == 'update':
    #     try:
    #         api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    #         api_response = api_client.update_domains(workload_domain_payload)
    #         payload_data = api_response.data
    #         module.exit_json(changed=True, data=payload_data)
    #     except:
    #         module.fail_json(msg="Failed to update workload domain")
    # elif validate == False and state == 'delete':
    #     '''
    #     To do:
    #     - Add Check for any VMs on clusters
    #     - Check for remote Datastores
    #     - Auto migrate VMs to other clusters in a different domain? 
    #     '''
    #     try:
    #         api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    #         api_response = api_client.delete_domains(workload_domain_payload)
    #         payload_data = api_response.data
    #         module.exit_json(changed=True, data=payload_data)
    #     except:
    #         module.fail_json(msg="Failed to delete workload domain")
    
if __name__ == '__main__':
    main()