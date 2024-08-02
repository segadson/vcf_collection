#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible_collections.vmware.vcf.plugins.module_utils.basic import *
from ansible_collections.vmware.vcf.plugins.module_utils.sddc_manager import SddcManagerApiClient
from ansible_collections.vmware.vcf.plugins.module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation

def get_edge_cluster_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, edge_cluster_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_edge_clusters()
    edge_clusters = api_response.data
    #print(type(edge_clusters))  # Check the type of edge_clusters
    #print(edge_clusters)  # Check the value of edge_clusters
    for edge_cluster in edge_clusters['elements']:  # Access the 'elements' key of the dictionary
        #print(type(edge_cluster))  # Check the type of each edge_cluster
        #print(edge_cluster)  # Check the value of each edge_cluster
        if edge_cluster['name'] == edge_cluster_name:
            return edge_cluster
    return None
def check_avn_current_operation(sddc_manager_ip, sddc_manager_user, sddc_manager_password):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_avns()
    payload_data = api_response.data
    return payload_data

def create_avns_(sddc_manager_ip, sddc_manager_user, sddc_manager_password, avns_payload):
    payload_data = avns_payload
    try:
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        api_response = api_client.create_avns(payload_data)
        payload_data = api_response.data
        return payload_data
    except VcfAPIException as e:
        raise VcfAPIException(f"Error: {e}")
        
        #Mimic This
        # try:
        #     api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        #     api_response = api_client.validate_domains(json.dumps(updated_workload_domain_payload))
        #     payload_data = api_response.data
        #     response = evaluate_response(payload_data)
        #     if response['message'] == "Successful":
        #         module.exit_json(changed=False, meta=payload_data)
        #     else:
        #         module.fail_json(msg="Workload Domain Validation Has Failed", meta=response)
        # except Exception as e:
        #     module.fail_json(msg="Failed to validate workload domain: " + str(e))
def validate_avns_(sddc_manager_ip, sddc_manager_user, sddc_manager_password, avns_payload):
    payload_data = avns_payload
    try:
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        api_response = api_client.validate_avns(payload_data)
        payload_data = api_response.data
        #print(f"Payload Data: {payload_data}")
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
        management_edge_cluster_name = dict(type='str', required=True)
    )

    module = AnsibleModule(supports_check_mode=True, argument_spec=parameters)
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    operation = module.params['operation']
    avns_payload = module.params['avns_payload']
    management_edge_cluster_name = module.params['management_edge_cluster_name']

    edge_cluster = get_edge_cluster_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, management_edge_cluster_name)
    if edge_cluster is None:
        module.fail_json(msg=f"Edge cluster {management_edge_cluster_name} not found")

    edge_cluster_id = edge_cluster['id']
    avns_payload['edgeClusterId'] = edge_cluster_id

    if operation == 'create':
        try:
            #print("Creating AVNs-Yes")
            payload_data = create_avns_(sddc_manager_ip, sddc_manager_user, sddc_manager_password, json.dumps(avns_payload))
            module.exit_json(changed=True, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")
    elif operation == 'validate':
        #print("Validating-Yes")
        try:
            payload_data = validate_avns_(sddc_manager_ip, sddc_manager_user, sddc_manager_password, json.dumps(avns_payload))
            #print(f"Payload Data: {payload_data}")
            module.exit_json(changed=True, meta=payload_data)
        except VcfAPIException as e:
            module.fail_json(msg=f"Error: {e}")

if __name__ == '__main__':
    main()