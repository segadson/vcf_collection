#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible.module_utils import basic
from ansible_collections.vmware.vcf.plugins.module_utils.sddc_manager import SddcManagerApiClient
from ansible_collections.vmware.vcf.plugins.module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

DOCUMENTATION = '''
---
module: sddc_manager_avns
short_description: This module manages the Application Virtual Networks (AVNs) in SDDC Manager
description:
    - "This module is a wrapper around the SDDC Manager AVNs API. It allows to create AVNs, get the current operation of AVNs, and get Edge Cluster by name."
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
    avns_payload:
        description:
            - The payload for the AVNs.
        required: false
        type: dict
    edge_cluster_name:
        description:
            - The name of the Edge Cluster.
        required: false
        type: str
requirements:
    - python >= 3.6
'''

EXAMPLES = '''
# How to use this module in your playbook
- name: Manage AVNs
  sddc_manager_avns:
    sddc_manager_ip: "192.168.1.1"
    sddc_manager_user: "admin"
    sddc_manager_password: "password"
    avns_payload: {"key": "value"}
'''

RETURN = '''
avns:
    description: The AVNs that were created or the current operation of AVNs.
    returned: always
    type: dict
edge_cluster:
    description: The Edge Cluster that was retrieved by name.
    returned: when edge_cluster_name is provided
    type: dict
'''

#Todo Documentation
class SDDCManagerAVNS:
    def __init__(self, module):
        self.module = module
        self.sddc_manager_ip = module.params['sddc_manager_ip']
        self.sddc_manager_user = module.params['sddc_manager_user']
        self.sddc_manager_password = module.params['sddc_manager_password']
        self.avns_payload = module.params['avns_payload']
        self.operation = module.params['operation']
        self.management_edge_cluster_name = module.params['management_edge_cluster_name']

    def get_edge_cluster_by_name(self):
        try:
            api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)
            api_response = api_client.get_edge_clusters()
            edge_clusters = api_response.data
        except Exception as e:
            self.module.fail_json(msg=f"Error: {e}")
        for edge_cluster in edge_clusters['elements']:
            if edge_cluster['name'] == self.management_edge_cluster_name:
                return edge_cluster
        return None

    def create_avns(self):
        edge_cluster = self.get_edge_cluster_by_name()
        if edge_cluster is None:
            self.module.fail_json(msg=f"Edge cluster {self.management_edge_cluster_name} not found")

        edge_cluster_id = edge_cluster['id']
        self.avns_payload['edgeClusterId'] = edge_cluster_id
        try:
            api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)
            api_response = api_client.create_avns(json.dumps(self.avns_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def validate_avns(self):
        edge_cluster = self.get_edge_cluster_by_name()
        if edge_cluster is None:
            self.module.fail_json(msg=f"Edge cluster {self.management_edge_cluster_name} not found")

        edge_cluster_id = edge_cluster['id']
        self.avns_payload['edgeClusterId'] = edge_cluster_id
        try:
            api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)
            api_response = api_client.validate_avns(json.dumps(self.avns_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def run(self):
        edge_cluster = self.get_edge_cluster_by_name()
        if edge_cluster is None:
            self.module.fail_json(msg=f"Edge cluster {self.management_edge_cluster_name} not found")

        edge_cluster_id = edge_cluster['id']
        self.avns_payload['edgeClusterId'] = edge_cluster_id

        if self.operation == 'create':
            return self.create_avns()
        elif self.operation == 'validate':
            return self.validate_avns()
def main():
    parameters = dict(
        sddc_manager_ip=dict(type='str', required=True),
        sddc_manager_user=dict(type='str', required=True),
        sddc_manager_password=dict(type='str', required=True, no_log=True),
        avns_payload=dict(type='dict', required=True),
        operation=dict(type='str', choices=['create', 'validate'], default='create'),
        management_edge_cluster_name=dict(type='str', required=True)
    )

    module = AnsibleModule(argument_spec=parameters, supports_check_mode=True)
    sddc_manager_avns = SDDCManagerAVNS(module)
    try:
        payload_data = sddc_manager_avns.run()
        module.exit_json(changed=True, meta=payload_data)
    except VcfAPIException as e:
        module.fail_json(msg=f"Error: {e}")

if __name__ == '__main__':
    main()