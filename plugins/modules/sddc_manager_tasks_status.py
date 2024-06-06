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
        "sddc_manager_password": {"required": True, "type": "str"},
        "validation": {"required": True, "type": "bool", "default": False},
        "sddc_manager_tasks_type": {"required": True, "type": "str","choices": ['wld_domain', 'avns', 'cluster', 'cluster_datastore',
                                                                                'hosts', 'nsxt_manager', 'nsxt_edge_cluster','sddc_upgrade']}
    }

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    tasks_id = module.params['tasks_id']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    validation = module.params['validation']
    sddc_manager_tasks_type = module.params['sddc_manager_tasks_type']

    def evaluate_tasks_status(payload_data):
        if payload_data['status'].upper() == 'FAILED':
            subtask_list = payload_data['subTasks']
            error_check_list = []
            for subtask in subtask_list:
                if subtask['status'].upper() == 'FAILED':
                    error_check_list.append(subtask)
            return error_check_list
        else:
            return payload_data

    validation_methods = {
        'nsxt_edge_cluster': 'edge_cluster_validation_status',
        'avns': 'validate_avns',
        'hosts': 'validate_hosts',
        'cluster': 'validate_clusters',
        'cluster_datastore': 'validate_mount_datastore_on_cluster',
        'wld_domain': 'validate_workload_domains',
        'sddc_upgrade': 'perform_sddc_manager_upgrade_prechecks'
    }

    try:
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        if validation:
            if sddc_manager_tasks_type in validation_methods:
                api_response = getattr(api_client, validation_methods[sddc_manager_tasks_type])(tasks_id)
                payload_data = api_response.data
                error_check_list = evaluate_tasks_status(payload_data)
                if error_check_list:
                    module.fail_json(msg=f"Error List: {error_check_list}")
                else:
                    module.exit_json(changed=False, meta=payload_data)
            else:
                module.fail_json(msg="Invalid Tasks To Monitor")
        else:
            api_response = api_client.get_sddc_manager_task_by_id(tasks_id)
            payload_data = api_response.data
            module.exit_json(changed=False, meta=payload_data)
    except VcfAPIException as e:
        module.fail_json(msg=f"Error: {e}")

if __name__ == '__main__':
    main()