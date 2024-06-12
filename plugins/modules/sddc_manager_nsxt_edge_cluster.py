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

def get_edge_cluster_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, edge_cluster_payload):
    edge_cluster_name = edge_cluster_payload['edgeClusterName']
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_edge_clusters()
    payload_data = api_response.data
    for element in payload_data['elements']:
        if element['name'] == edge_cluster_name:
            return element
    return None



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
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    edge_cluster_payload = module.params['edge_cluster_payload']
    validate = module.params['validate']
    management_cluster_name = module.params['management_cluster_name']
    state = module.params['state']

    def get_host_cluster_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, management_cluster_name):
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        api_response = api_client.get_clusters_all_clusters()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == management_cluster_name:
                return element
        return None


    def get_edge_cluster_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, edge_cluster_payload):
        edge_cluster_name = edge_cluster_payload['edgeClusterName']
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        api_response = api_client.get_edge_clusters()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == edge_cluster_name:
                return element
        return None

    if state == 'create' and validate == True:

        #Add Cluster ID to Payload
        current_state = get_host_cluster_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, management_cluster_name)
        mgmt_cluster_id = current_state['id']
        for cluster in edge_cluster_payload['edgeNodeSpecs']:
            cluster['clusterId'] = mgmt_cluster_id
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_edge_cluster(json.dumps(edge_cluster_payload))
            payload_data = api_response.data
            module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")

    elif state == 'create' and validate == False:

        #Add Cluster ID to Payload
        current_state = get_host_cluster_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, management_cluster_name)
        mgmt_cluster_id = current_state['id']
        for cluster in edge_cluster_payload['edgeNodeSpecs']:
            cluster['clusterId'] = mgmt_cluster_id['id']
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.create_edge_cluster(json.dumps(edge_cluster_payload))
            payload_data = api_response.data
            module.exit_json(changed=True, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")
    elif state == 'expand_or_shrink' and validate == False:
        current_state = get_edge_cluster_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, edge_cluster_payload['edgeClusterName'])
        edge_cluster_id = current_state['id']
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.expand_or_shrink_edge_cluster(edge_cluster_id, json.dumps(edge_cluster_payload))
            payload_data = api_response.data
            module.exit_json(changed=True, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")

    elif state == 'expand_or_shrink' and validate == True:
        current_state = get_edge_cluster_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, edge_cluster_payload['edgeClusterName'])
        edge_cluster_id = current_state['id']
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_edge_cluster(edge_cluster_id, json.dumps(edge_cluster_payload))
            payload_data = api_response.data
            module.exit_json(changed=False, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")

    else:
        module.fail_json(msg="Error: Invalid State")
    
if __name__ == '__main__':
    main()