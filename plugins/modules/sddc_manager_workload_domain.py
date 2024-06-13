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
    parameters = dict(
    sddc_manager_ip=dict(type='str', required=True),
    sddc_manager_user=dict(type='str', required=True),
    sddc_manager_password=dict(type='str', required=True, no_log=True),
    state=dict(type='str', choices=['create', 'delete', 'validate'], required=True),
    workload_domain_payload=dict(type='dict', required=True),
    license_key=dict(type='str', required=True),
    nsx_license_key=dict(type='str', required=True),
    hosts_list_payload=dict(type='dict', required=True)
)

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    workload_domain_payload = module.params['workload_domain_payload']
    license_key = module.params['license_key']
    nsx_license_key = module.params['nsx_license_key']
    hosts_list_payload = module.params['hosts_list_payload']
    state = module.params['state']

    

    def get_host_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, name):
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.get_all_hosts()
            payload_data = api_response.data
            for element in payload_data['elements']:
                if element['fqdn'] == name:
                    return element
        except Exception as e:
            module.fail_json(msg="Failed to get host by name: " + str(e))

    def create_workload_domain_payload(workload_domain_payload, hosts_list_payload):
        clusters = workload_domain_payload['computeSpec']['clusterSpecs']
        for cluster_specs in clusters:
            host_specs = []
            host_network_spec = cluster_specs['hostNetworkSpec']
            for host in hosts_list_payload['hosts']:
                host
                host_name = host['fqdn']
                host_data = get_host_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, host_name)
                host['id'] = host_data['id']
                host['licenseKey'] = license_key
                host_spec = {}
                host_spec['hostId'] = host['id']
                host_spec['licenseKey'] = host['licenseKey']
                host_spec['hostNetworkSpec'] = host_network_spec
                host_specs.append(host_spec)


    if state == 'validate':
        updated_workload_domain_payload = create_workload_domain_payload(workload_domain_payload, hosts_list_payload)
        updated_workload_domain_payload['nsxTSpec']['licenseKey'] = nsx_license_key
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_domains(updated_workload_domain_payload)
            print(api_response)
            payload_data = api_response["data"]
            module.exit_json(changed=False, meta=payload_data)
        except Exception as e:
            module.fail_json(msg="Failed to validate workload domain: " + str(e))
    elif state == 'create':
        updated_workload_domain_payload = create_workload_domain_payload(workload_domain_payload, hosts_list_payload)
        updated_workload_domain_payload['nsxTSpec']['licenseKey'] = nsx_license_key
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.create_domains(updated_workload_domain_payload)
            payload_data = api_response["data"]
            module.exit_json(changed=True, meta=payload_data)
        except:
            module.fail_json(msg="Failed to create workload domain")
    elif state == 'update':
        updated_workload_domain_payload = create_workload_domain_payload(workload_domain_payload, hosts_list_payload)
        updated_workload_domain_payload['nsxTSpec']['licenseKey'] = nsx_license_key
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.update_domains(updated_workload_domain_payload)
            payload_data = api_response["data"]
            module.exit_json(changed=True, meta=payload_data)
        except:
            module.fail_json(msg="Failed to update workload domain")
    elif state == 'delete':
        '''
        To do:
        - Add Check for any VMs on clusters
        - Check for remote Datastores
        - Auto migrate VMs to other clusters in a different domain? 
        '''
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.delete_domains(updated_workload_domain_payload)
            payload_data = api_response["data"]
            module.exit_json(changed=True, meta=payload_data)
        except:
            module.fail_json(msg="Failed to delete workload domain")
    
if __name__ == '__main__':
    main()

