#!/usr/bin/python
import os
import sys


# current_dir = os.path.dirname(os.path.realpath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
DOCUMENTATION = '''

module: sddc_manager_tasks_status
short_description: Get the status of a task in SDDC Manager
description:

    - This module allows you to get the status of a task in SDDC Manager.
version_added: "2.9"
options:
    sddc_manager_ip:
        description:
            - The IP address of the SDDC Manager.
        required: true  
    tasks_id:   
        description:
            - The ID of the task.
        required: true
    sddc_manager_user:
        description:
            - The username to authenticate with the SDDC Manager.
        required: true
    sddc_manager_password:
        description:
            - The password to authenticate with the SDDC Manager.
        required: true
    validation:
        description:
            - Whether to validate the task.
        required: true
        type: bool
    sddc_manager_tasks_type:
        description:
            - The type of the task.
        required: true  
        choices: ['wld_domain', 'avns', 'clusters', 'cluster_datastore', 'hosts', 'nsxt_manager', 'nsxt_edge_cluster','sddc_upgrade']
'''
from ansible_collections.vmware.vcf.plugins.moduleutils.basic import *
from ansible_collections.vmware.vcf.plugins.moduleutils.sddc_manager import SddcManagerApiClient
from ansible_collections.vmware.vcf.plugins.moduleutils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

   
class SddcManagerTaskProcessor:
    def __init__(self, module):
        self.module = module
        self.sddc_manager_ip = module.params['sddc_manager_ip']
        self.tasks_id = module.params['tasks_id']
        self.sddc_manager_user = module.params['sddc_manager_user']
        self.sddc_manager_password = module.params['sddc_manager_password']
        self.validation = module.params['validation']
        self.sddc_manager_tasks_type = module.params['sddc_manager_tasks_type']
        self.api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)

    def evaluate_tasks_status(self, payload_data):
        if payload_data['status'] == 'FAILED':
            error_check_list = payload_data['errors']
            self.module.fail_json(changed=False, meta=error_check_list)
        else:
            self.module.exit_json(changed=True, meta=payload_data)

    def evaluate_validation_status(self, payload_data):
        if payload_data['executionStatus'] == 'FAILED':
            validation_check_list = payload_data['validationChecks']
            error_check_list = [check for check in validation_check_list if check['resultStatus'] == 'FAILED']
            self.module.fail_json(changed=False, meta=error_check_list)
        else:
            self.module.exit_json(changed=False, meta=payload_data)

    def process_validation_task(self, api_call_method):
        try:
            api_response = api_call_method(self.tasks_id)
            payload_data = api_response.data
            self.evaluate_validation_status(payload_data)
        except VcfAPIException as e:
            self.module.fail_json(changed=False, meta=str(e))

    def process_tasks(self):
        if self.validation:
            method_mapping = {
                'nsxt_edge_cluster': self.api_client.edge_cluster_validation_status,
                'avns': self.api_client.validate_avns,
                'hosts': self.api_client.get_validate_hosts_status,
                'clusters': self.api_client.validate_clusters,
                'cluster_datastore': self.api_client.validate_mount_datastore_on_cluster,
                'sddc_upgrade': self.api_client.perform_sddc_manager_upgrade_prechecks
            }
            api_call_method = method_mapping.get(self.sddc_manager_tasks_type)
            if api_call_method:
                self.process_validation_task(api_call_method)
            else:
                self.module.fail_json(changed=False, msg="Invalid Tasks To Monitor")
        else:
            self.process_non_validation_task()

    def process_non_validation_task(self):
        try:
            api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)
            api_response = api_client.get_sddc_manager_task_by_id(self.tasks_id)
            payload_data = api_response.data
            self.evaluate_tasks_status(payload_data)
        except VcfAPIException as e:
            self.module.fail_json(changed=False, meta=str(e))
    @staticmethod
    def run():
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
        module = AnsibleModule(supports_check_mode=True, argument_spec=parameters)
        processor = SddcManagerTaskProcessor(module)
        processor.process_tasks()

if __name__ == '__main__':
    SddcManagerTaskProcessor.run()