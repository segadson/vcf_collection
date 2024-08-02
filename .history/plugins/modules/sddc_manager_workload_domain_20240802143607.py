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
Document = '''
query: sddc_manager_workload_domain
short_description: Create, Delete, or Validate Workload Domains
description:
    - This module allows you to create, delete, or validate a workload domain in SDDC Manager.
version_added: "2.9"
options:
    sddc_manager_ip:
        description:
            - The IP address of the SDDC Manager.
        required: true
    sddc_manager_user:
        description:
            - The username to authenticate with the SDDC Manager.
        required: true
    sddc_manager_password:  
        description:
            - The password to authenticate with the SDDC Manager.
        required: true  
    state:
        description:
            - The state of the workload domain.
        required: true
        choices: ['create', 'delete', 'validate']
    workload_domain_payload:
        description:
            - The payload for the workload domain.
        required: true
    license_key:
        description:
            - The license key for the workload domain.
        required: true
    nsx_license_key:
        description:
            - The NSX license key for the workload domain.
        required: true  
    vsan_license_key:   
        description:
            - The vSAN license key for the workload domain.
        required: false 
    hostsSpec:  
        description:
            - The hosts for the workload domain.
        required: true  
'''

class SddcManagerWorkloadDomain:
    def __init__(self, module):
        self.module = module
        self.sddc_manager_ip = module.params['sddc_manager_ip']
        self.sddc_manager_user = module.params['sddc_manager_user']
        self.sddc_manager_password = module.params['sddc_manager_password']
        self.workload_domain_payload = module.params['workload_domain_payload']
        self.license_key = module.params['license_key']
        self.nsx_license_key = module.params['nsx_license_key']
        self.vsan_license_key = module.params['vsan_license_key']
        self.hostsSpec = module.params['hostsSpec']
        self.state = module.params['state']
        self.api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)

    def get_host_by_name(self, name):
        try:
            api_response = self.api_client.get_all_hosts()
            payload_data = api_response.data
            for element in payload_data['elements']:
                if element['fqdn'] == name:
                    return element
        except Exception as e:
            self.module.fail_json(msg="Failed to get host by name: " + str(e))

    def create_workload_domain_payload(self):
        clusters = self.workload_domain_payload['computeSpec']['clusterSpecs']
        host_specs = []
        for cluster_specs in clusters:
            host_network_spec = cluster_specs['hostNetworkSpec']
            for host in self.hostsSpec['hosts']:
                host
                host_name = host['fqdn']
                host_data = self.get_host_by_name(host_name)
                host['id'] = host_data['id']
                host['licenseKey'] = self.license_key
                host_spec = {}
                host_spec['id'] = host['id']
                host_spec['licenseKey'] = host['licenseKey']
                host_spec['hostNetworkSpec'] = host_network_spec
                host_specs.append(host_spec)
            cluster_specs['hostSpecs'] = host_specs
            #This is for vSAN CLusters will need to update for vVol, NFS, etc
            cluster_specs['datastoreSpec']['vsanDatastoreSpec']['licenseKey'] = self.vsan_license_key
        return self.workload_domain_payload

    def evaluate_response(self, data):
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
    
    def validate_workload_domain(self):
        updated_workload_domain_payload = self.create_workload_domain_payload()
        updated_workload_domain_payload['nsxTSpec']['licenseKey'] = self.nsx_license_key
        if "hostNetworkSpec" in self.workload_domain_payload:
            del self.workload_domain_payload["hostNetworkSpec"]
        try:
            api_response = self.api_client.validate_domains(json.dumps(updated_workload_domain_payload))
            payload_data = api_response.data
            response = self.evaluate_response(payload_data)
            if response['message'] == "Successful":
                return payload_data
            else:
                return response
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def create_workload_domain(self):
        updated_workload_domain_payload = self.create_workload_domain_payload()
        updated_workload_domain_payload['nsxTSpec']['licenseKey'] = self.nsx_license_key
        if "hostNetworkSpec" in self.workload_domain_payload:
            del self.workload_domain_payload["hostNetworkSpec"]
        
        try:
            api_response = self.api_client.create_domains(json.dumps(updated_workload_domain_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def delete_workload_domain(self):
        '''
        To Do:
        check for VMs on clusters
        '''
        try:
            api_response = self.api_client.delete_domains(json.dumps(self.workload_domain_payload))
            payload_data = api_response.data
            return payload_data
        except VcfAPIException as e:
            self.module.fail_json(msg=f"Error: {e}")

    def run(self):
        if self.state == 'validate':
            result = self.validate_workload_domain()
            self.module.exit_json(changed=False, meta=result)
        elif self.state == 'create':
            result = self.create_workload_domain()
            self.module.exit_json(changed=True, meta=result)
        elif self.state == 'delete':
            result = self.delete_workload_domain()
            self.module.exit_json(changed=True, meta=result)
        else:
            self.module.fail_json(msg="Not Valid Action")

def main():
    parameters = dict(
        sddc_manager_ip=dict(required=True, type='str'),
        sddc_manager_user=dict(required=True, type='str'),
        sddc_manager_password=dict(required=True, type='str'),
        workload_domain_payload=dict(required=True, type='dict'),
        license_key=dict(required=True, type='str'),
        nsx_license_key=dict(required=True, type='str'),
        vsan_license_key=dict(required=False, type='str'),
        hostsSpec=dict(required=True, type='dict'),
        state=dict(required=True, choices=['create', 'delete', 'validate'])
    )

    module = AnsibleModule(supports_check_mode=True, argument_spec=parameters)
    workload_domain = SddcManagerWorkloadDomain(module)
    workload_domain.run()

if __name__ == '__main__':
    main()