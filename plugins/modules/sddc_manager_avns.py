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

def check_avn_current_operation(sddc_manager_ip, sddc_manager_user, sddc_manager_password):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_avns()
    payload_data = api_response['data']
    return payload_data

def create_avns_(sddc_manager_ip, sddc_manager_user, sddc_manager_password, avns_payload):
    payload_data = avns_payload
    try:
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        api_response = api_client.create_avns(payload_data)
        payload_data = api_response['data']
        return payload_data
    except VcfAPIException as e:
        raise VcfAPIException(f"Error: {e}")

def validate_avns_(sddc_manager_ip, sddc_manager_user, sddc_manager_password, avns_payload):
    payload_data = avns_payload
    try:
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        api_response = api_client.validate_avns(payload_data)
        payload_data = api_response['data']
        return payload_data
    except VcfAPIException as e:
        raise VcfAPIException(f"Error: {e}")

def main():
    parameters = dict(
        sddc_manager_ip=dict(type='str', required=True),
        sddc_manager_user=dict(type='str', required=True),
        sddc_manager_password=dict(type='str', required=True, no_log=True),
        avns_payload=dict(type='dict', required=True),
        operation=dict(type='str', choices=['create', 'validate'], default='create'),
    )

    module = AnsibleModule(supports_check_mode=True, argument_spec=parameters)
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    operation = module.params['operation']
    avns_payload = module.params['avns_payload']

    if operation == 'create':
        try:
            print("Creating AVNs-Yes")
            payload_data = create_avns_(sddc_manager_ip, sddc_manager_user, sddc_manager_password, json.dumps(avns_payload))
            module.exit_json(changed=True, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")
    elif operation == 'validate':
        print("Validating-Yes")
        try:
            payload_data = validate_avns_(sddc_manager_ip, sddc_manager_user, sddc_manager_password, json.dumps(avns_payload))
            module.exit_json(changed=True, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")

if __name__ == '__main__':
    main()