#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible.module_utils.basic import *
from ansible.module_utils.sddc_manager import SddcManagerApiClient
from ansible.module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation
def main():
    parameters = {
        "sddc_manager_ip": {"required": True, "type": "str"},
        "tasks_id": {"required": True, "type": "str"},
        "sddc_manager_user": {"required": True, "type": "str"},
        "sddc_manager_password": {"required": True, "type": "str", "no_log": True},
        "validation": {"type": "bool", "required": True},
        "sddc_manager_tasks_type": {
            "required": True, 
            "type": "str",
            "choices": ['wld_domain', 'avns', 'clusters', 'cluster_datastore', 'hosts', 'nsxt_manager', 'nsxt_edge_cluster','sddc_upgrade']
        }
    }
    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    tasks_id = module.params['tasks_id']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    validation = module.params['validation']
    sddc_manager_tasks_type = module.params['sddc_manager_tasks_type']

    print(sddc_manager_tasks_type)
    print(validation)

    def evaluate_tasks_status(payload_data):
        if payload_data['status'] == 'FAILED':
            error_check_list = payload_data['errors']
            module.fail_json(changed=False, meta=error_check_list)
        else:
            module.exit_json(changed=True, meta=payload_data)
        
    def evaluate_validation_status(payload_data):
        if payload_data['executionStatus'] == 'FAILED':
            validation_check_list = payload_data['validationChecks']
            error_check_list = []
            for validation_check in validation_check_list:
                if validation_check['resultStatus'] == 'FAILED':
                    error_check_list.append(validation_check)

            module.fail_json(changed=False, meta=error_check_list)
        else:
            module.exit_json(changed=False, meta=payload_data) # return an empty list when resultStatus is not 'FAILED'
        
    if validation == True and sddc_manager_tasks_type == 'nsxt_edge_cluster':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.edge_cluster_validation_status(tasks_id)
            payload_data = api_response.data
            error_check_list = evaluate_validation_status(payload_data)

        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'avns':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_avns(tasks_id)
            payload_data = api_response.data
            error_check_list = evaluate_validation_status(payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'hosts':
        payload_data = None
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.get_validate_hosts_status(tasks_id)
            print(api_response)
            payload_data = api_response.data
            error_check_list = evaluate_validation_status(payload_data)
        except VcfAPIException as e:
            module.fail_json(msg="An error occurred during the API call", changed=False, meta=e)
    elif validation == True and sddc_manager_tasks_type == 'clusters':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_clusters(tasks_id)
            payload_data = api_response.data
            error_check_list = evaluate_validation_status(payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'cluster_datastore':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_mount_datastore_on_cluster(tasks_id)
            payload_data = api_response.data
            error_check_list = evaluate_validation_status(payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    # elif validation == True and sddc_manager_tasks_type == 'wld_domain':
    #     try:
    #         api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    #         api_response = api_client.get_domain_validation_status(tasks_id)
    #         payload_data = api_response.data
    #         error_check_list = evaluate_validation_status(payload_data)
    #     except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'sddc_upgrade':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.perform_sddc_manager_upgrade_prechecks(tasks_id)
            payload_data = api_response.data
            error_check_list = evaluate_validation_status(payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == False:
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.get_sddc_manager_task_by_id(tasks_id)
            payload_data = api_response.data
            tasks_status = evaluate_tasks_status(payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    else:
        module.fail_json(changed=False, msg="Invalid Tasks To Monitor")

if __name__ == '__main__':
    main()

    