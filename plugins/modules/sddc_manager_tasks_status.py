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
        "tasks_id": {"required": True, "type": "str"},
        "sddc_manager_user": {"required": True, "type": "str"},
        "sddc_manager_password": {"required": True, "type": "str", "no_log": True},
        "validation": {"type": "bool", "default": False},
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
            subtask_list = payload_data['subTasks']
            error_check_list = []
            for subtask in subtask_list:
                if subtask['status'].upper() == 'FAILED':
                    error_check_list.append(subtask)
            return error_check_list
        else:
            return []  # return an empty list when resultStatus is not 'FAILED'
        
    def evaluate_validation_status(payload_data):
        if payload_data['resultStatus'] == 'FAILED':
            validation_list = payload_data['validationChecks']
            error_check_list = []
            for validation in validation_list:
                if validation['resultStatus'].upper() == 'FAILED':
                    error_check_list.append(validation)
            return error_check_list
        else:
            return []  # return an empty list when resultStatus is not 'FAILED'
        
    if validation == True and sddc_manager_tasks_type == 'nsxt_edge_cluster':
        try:
            
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.edge_cluster_validation_status(tasks_id)
            payload_data = api_response
            error_check_list = evaluate_validation_status(payload_data)
            if error_check_list:
                module.fail_json(changed=False, meta=payload_data)
            else:
                module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'avns':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_avns(tasks_id)
            payload_data = api_response
            error_check_list = evaluate_validation_status(payload_data)
            if error_check_list:
                module.fail_json(changed=False, meta=payload_data)
            else:
                module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'hosts':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_hosts(tasks_id)
            payload_data = api_response
            error_check_list = evaluate_validation_status(payload_data)
            if error_check_list:
                module.fail_json(changed=False, meta=payload_data)
            else:
                module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'clusters':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_clusters(tasks_id)
            payload_data = api_response
            error_check_list = evaluate_validation_status(payload_data)
            if error_check_list:
                module.fail_json(changed=False, meta=payload_data)
            else:
                module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'cluster_datastore':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_mount_datastore_on_cluster(tasks_id)
            payload_data = api_response
            error_check_list = evaluate_validation_status(payload_data)
            if error_check_list:
                module.fail_json(changed=False, meta=payload_data)
            else:
                module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'wld_domain':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_domains(tasks_id)
            payload_data = api_response
            error_check_list = evaluate_validation_status(payload_data)
            if error_check_list:
                module.fail_json(changed=False, meta=payload_data)
            else:
                module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == True and sddc_manager_tasks_type == 'sddc_upgrade':
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.perform_sddc_manager_upgrade_prechecks(tasks_id)
            payload_data = api_response
            error_check_list = evaluate_validation_status(payload_data)
            if error_check_list:
                module.fail_json(changed=False, meta=payload_data)
            else:
                module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    elif validation == False:
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.get_sddc_manager_task_by_id(tasks_id)
            payload_data = api_response
            failed_tasks = evaluate_tasks_status(payload_data)
            if failed_tasks:
                module.fail_json(changed=False, meta=payload_data)
            else:
                module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(changed=False, meta=payload_data)
    else:
        module.fail_json(changed=False, msg="Invalid Tasks To Monitor")

if __name__ == '__main__':
    main()

    