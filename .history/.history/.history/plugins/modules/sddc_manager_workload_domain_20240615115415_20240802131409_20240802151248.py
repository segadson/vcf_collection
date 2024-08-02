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
    vsan_license_key=dict(type='str', required=False),
    hostsSpec=dict(type='dict', required=True)
)

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    workload_domain_payload = module.params['workload_domain_payload']
    license_key = module.params['license_key']
    nsx_license_key = module.params['nsx_license_key']
    vsan_license_key = module.params['vsan_license_key']
    hostsSpec = module.params['hostsSpec']
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

    #Todo: Clean This up
    def create_workload_domain_payload(workload_domain_payload, hostsSpec):
        clusters = workload_domain_payload['computeSpec']['clusterSpecs']
        host_specs = []
        for cluster_specs in clusters:
            host_network_spec = cluster_specs['hostNetworkSpec']
            for host in hostsSpec['hosts']:
                host
                host_name = host['fqdn']
                host_data = get_host_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, host_name)
                host['id'] = host_data['id']
                host['licenseKey'] = license_key
                host_spec = {}
                host_spec['id'] = host['id']
                host_spec['licenseKey'] = host['licenseKey']
                host_spec['hostNetworkSpec'] = host_network_spec
                host_specs.append(host_spec)
            cluster_specs['hostSpecs'] = host_specs
            #This is for vSAN CLusters will need to update for vVol, NFS, etc
            cluster_specs['datastoreSpec']['vsanDatastoreSpec']['licenseKey'] = vsan_license_key
        return workload_domain_payload

    def evaluate_response(data):
        output = {}
        if data['resultStatus'] == 'FAILED':
            for check in data['validationChecks']:
                if check['resultStatus'] == 'FAILED':
                    output['errorCode'] = check['errorResponse']['errorCode']
                    output['arguments'] = check['errorResponse']['arguments']
                    output['message'] = check['errorResponse']['message']
        else:
            output['message'] = "Successful"
        return output


    if state == 'validate':
        updated_workload_domain_payload = create_workload_domain_payload(workload_domain_payload, hostsSpec)
        updated_workload_domain_payload['nsxTSpec']['licenseKey'] = nsx_license_key
        if "hostNetworkSpec" in workload_domain_payload:
            del workload_domain_payload["hostNetworkSpec"]

        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.validate_domains(json.dumps(updated_workload_domain_payload))
            payload_data = api_response.data
            response = evaluate_response(payload_data)
            if response['message'] == "Successful":
                module.exit_json(changed=False, meta=payload_data)
            else:
                module.fail_json(msg="Workload Domain Validation Has Failed", meta=response)
        except Exception as e:
            module.fail_json(msg="Failed to validate workload domain: " + str(e))
    elif state == 'create':
        updated_workload_domain_payload = create_workload_domain_payload(workload_domain_payload, hostsSpec)
        updated_workload_domain_payload['nsxTSpec']['licenseKey'] = nsx_license_key
        if "hostNetworkSpec" in workload_domain_payload:
            del workload_domain_payload["hostNetworkSpec"]
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.create_domains(json.dumps(updated_workload_domain_payload))
            payload_data = api_response.data
            module.exit_json(changed=True, meta=payload_data)
        except Exception as e:
            module.fail_json(msg="Failed to create workload domain", exception=str(e), stdout=e.stdout if hasattr(e, 'stdout') else None, stderr=e.stderr if hasattr(e, 'stderr') else None)
    elif state == 'update':
        updated_workload_domain_payload = create_workload_domain_payload(workload_domain_payload, hostsSpec)
        updated_workload_domain_payload['nsxTSpec']['licenseKey'] = nsx_license_key
        if "hostNetworkSpec" in workload_domain_payload:
            del workload_domain_payload["hostNetworkSpec"]
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.update_domains(json.dumps(updated_workload_domain_payload))
            payload_data = api_response.data
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
            api_response = api_client.delete_domains(json.dumps(updated_workload_domain_payload))
            payload_data = api_response.data
            module.exit_json(changed=True, meta=payload_data)
        except:
            module.fail_json(msg="Failed to delete workload domain")
    
if __name__ == '__main__':
    main()

