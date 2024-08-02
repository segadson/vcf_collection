#!/usr/bin/python

from ansible_collections.vmware.vcf.plugins.moduleutils.basic import AnsibleModule
from ansible_collections.vmware.vcf.plugins.moduleutils.sddc_manager import SddcManagerApiClient
from ansible_collections.vmware.vcf.plugins.moduleutils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

DOCUMENTATION = '''
---
module: sddc_manager_nsxt_edge_cluster
short_description: This module manages NSX-T Edge Clusters in SDDC Manager
description:
    - "This module is a wrapper around the SDDC Manager NSX-T Edge Clusters API. It allows to create, delete, and expand or shrink NSX-T Edge Clusters."
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
    edge_cluster_payload:
        description:
            - The payload for the Edge Cluster.
        required: false
        type: dict
    validate:
        description:
            - Whether to validate the Edge Cluster.
        required: false
        type: bool
        default: false
    management_cluster_name:
        description:
            - The name of the management cluster.
        required: false
        type: str
    state:
        description:
            - The state of the Edge Cluster. Choices are 'create', 'delete', 'expand_or_shrink'.
        required: true
        type: str
requirements:
    - python >= 3.6
'''

EXAMPLES = '''
# How to use this module in your playbook
- name: Manage NSX-T Edge Cluster
  sddc_manager_nsxt_edge_cluster:
    sddc_manager_ip: "192.168.1.1"
    sddc_manager_user: "admin"
    sddc_manager_password: "password"
    state: "create"
'''

RETURN = '''
edge_cluster:
    description: The Edge Cluster that was created, deleted, or modified.
    returned: always
    type: dict
'''
class EdgeClusterManager:
    def __init__(self, module):
        self.module = module
        self.sddc_manager_ip = module.params['sddc_manager_ip']
        self.sddc_manager_user = module.params['sddc_manager_user']
        self.sddc_manager_password = module.params['sddc_manager_password']
        self.state = module.params['state']
        self.validate = module.params['validate']
    #Functions
    def get_host_cluster_by_name(self, management_cluster_name):
        try:
            api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)
            api_response = api_client.get_clusters_all_clusters()
            payload_data = api_response.data
            for element in payload_data['elements']:
                if element['name'] == management_cluster_name:
                    return element
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")
    
    def get_edge_cluster_by_name(self, edge_cluster_name):
        try:
            api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)
            api_response = api_client.get_edge_clusters()
            payload_data = api_response.data
            for element in payload_data['elements']:
                if element['name'] == edge_cluster_name:
                    return element
            return None
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")
    def create(self):
        # Add Module Parameters
        management_cluster_name = self.module.params['management_cluster_name']
        edge_cluster_payload = self.module.params['edge_cluster_payload']

        host_cluster = self.get_host_cluster_by_name(management_cluster_name)
        host_cluster_id = host_cluster['id']
        for cluster in edge_cluster_payload['edgeNodeSpecs']:
            cluster['clusterId'] = host_cluster_id
        try:
            api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)
            api_response = api_client.create_edge_cluster(json.dumps(edge_cluster_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def validation(self):
        # Add Module Parameters
        management_cluster_name = self.module.params['management_cluster_name']
        edge_cluster_payload = self.module.params['edge_cluster_payload']

        host_cluster = self.get_host_cluster_by_name(management_cluster_name)
        host_cluster_id = host_cluster['id']
        for cluster in edge_cluster_payload['edgeNodeSpecs']:
            cluster['clusterId'] = host_cluster_id
        try:
            api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)
            api_response = api_client.validate_edge_cluster(json.dumps(edge_cluster_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")
    def expand_or_shrink(self):
        # Add Module Parameters
        edge_cluster_name = self.module.params['edge_cluster_name']
        edge_cluster_payload = self.module.params['edge_cluster_payload']   

        edge_cluster = self.get_edge_cluster_by_name(edge_cluster_name)
        edge_cluster_id = edge_cluster['id']
        try:
            api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)
            api_response = api_client.expand_or_shrink_edge_cluster(edge_cluster_id, json.dumps(edge_cluster_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")
    def run(self):
        if self.state == 'create' and self.validate == False:
            result = self.create()
            self.module.exit_json(changed=True, meta=result)
        elif self.state == 'create' and self.validate == True:
            result = self.validation()
            self.module.exit_json(changed=False, meta=result)
        elif self.state == 'expand_or_shrink' and self.validate == False:
            result = self.expand_or_shrink()
            self.module.exit_json(changed=True, meta=result)
        elif self.state == 'expand_or_shrink' and self.validate == True:
            result = self.validation()
            self.module.exit_json(changed=False, meta=result)
        else:
            self.module.fail_json(msg="Error: Invalid State")

def main():
    parameters = {
        "sddc_manager_ip": {"required": True, "type": "str"},
        "sddc_manager_user": {"required": True, "type": "str"},
        "sddc_manager_password": {"required": True, "type": "str"},
        "edge_cluster_payload": {"required": False, "type": "dict"},
        "validate": {"required": False, "type": "bool", "default": False},
        "management_cluster_name": {"required": False, "type": "str"},
        "state": {"required": True, "type": "str", "choices": ['create', 'delete', 'expand_or_shrink']}
        
    }

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    manager = EdgeClusterManager(module)
    manager.run()

if __name__ == '__main__':
    main()

