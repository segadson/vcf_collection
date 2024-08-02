#!/usr/bin/python
import os
import sys




from ansible.module_utils import basic
from ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder import CloudBuilderApiClient
from ansible_collections.vmware.vcf.plugins.module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

DOCUMENTATION = '''
---
module: cloud_builder_sddc_validation
short_description: Ansible module for validating SDDC management domain using Cloud Builder API
description:
    - "This module connects to the Cloud Builder API and validates the SDDC management domain using the provided parameters."
    - "It requires the following parameters:"
    - "cloud_builder_ip: IP address of the Cloud Builder"
    - "cloud_builder_user: Username for authentication with the Cloud Builder"
    - "cloud_builder_password: Password for authentication with the Cloud Builder"
    - "sddc_management_domain_payload: Payload containing the SDDC management domain details"
    - "The module returns the validation result as a JSON object."
version_added: "2.9"
author: "Sean Gadson"
options:
    cloud_builder_ip:
        description:
            - IP address of the Cloud Builder
        required: true
    cloud_builder_user:
        description:
            - Username for authentication with the Cloud Builder
        required: true
    cloud_builder_password:
        description:
            - Password for authentication with the Cloud Builder
        required: true
    sddc_management_domain_payload:
        description:
            - Payload containing the SDDC management domain details
        required: true
'''

RETURN = '''
meta:
    description: Validation result
    type: dict
'''

EXAMPLES = '''
- name: Validate SDDC management domain
    cloud_builder_sddc_validation:
        cloud_builder_ip: "{{ cloud_builder_ip }}"
        cloud_builder_user: "{{ cloud_builder_user }}"
        cloud_builder_password: "{{ cloud_builder_password }}"
        sddc_management_domain_payload:
            name: "{{ sddc_name }}"
            region: "{{ region }}"
            sddc_type: "{{ sddc_type }}"
            num_hosts: "{{ num_hosts }}"
            provider: "{{ provider }}"
            vpc_cidr: "{{ vpc_cidr }}"
            vpc_id: "{{ vpc_id }}"
            vpc_subnet_cidr: "{{ vpc_subnet_cidr }}"
            vpc_subnet_id: "{{ vpc_subnet_id }}"
            sddc_management_subnet_cidr: "{{ sddc_management_subnet_cidr }}"
            sddc_management_subnet_id: "{{ sddc_management_subnet_id }}"
            sddc_management_subnet_az: "{{ sddc_management_subnet_az }}"
            sddc_management_subnet_gateway: "{{ sddc_management_subnet_gateway }}"
            sddc_management_subnet_dns_servers: "{{ sddc_management_subnet_dns_servers }}"
            sddc_management_subnet_ntp_servers: "{{ sddc_management_subnet_ntp_servers }}"
            sddc_management_subnet_cidr: "{{ sddc_management_subnet_cidr }}"
            sddc_management_subnet_id: "{{ sddc_management_subnet_id }}"
            sddc_management_subnet_az: "{{ sddc_management_subnet_az }}"
            sddc_management_subnet_gateway: "{{ sddc_management_subnet_gateway }}"
            sddc_management_subnet_dns_servers: "{{ sddc_management_subnet_dns_servers }}"
            sddc_management_subnet_ntp_servers: "{{ sddc_management_subnet_ntp_servers }}"
            sddc_management_subnet_cidr: "{{ sddc_management_subnet_cidr }}"
            sddc_management_subnet_id: "{{ sddc_management_subnet_id }}"
            sddc_management_subnet_az: "{{ sddc_management_subnet_az }}"
            sddc_management_subnet_gateway: "{{ sddc_management_subnet_gateway }}"
            sddc_management_subnet_dns_servers: "{{ sddc_management_subnet_dns_servers }}"
            sddc_management_subnet_ntp_servers: "{{ sddc_management_subnet_ntp_servers }}"

'''


def main():
    """
    Ansible module for validating SDDC management domain using Cloud Builder API.

    This module connects to the Cloud Builder API and validates the SDDC management domain
    using the provided parameters. It requires the following parameters:
    - cloud_builder_ip: IP address of the Cloud Builder
    - cloud_builder_user: Username for authentication with the Cloud Builder
    - cloud_builder_password: Password for authentication with the Cloud Builder
    - sddc_management_domain_payload: Payload containing the SDDC management domain details

    The module returns the validation result as a JSON object.

    :return: JSON object containing the validation result
    """
    parameters = {
        "cloud_builder_ip": {"required": True, "type": "str"},
        "cloud_builder_user": {"required": True, "type": "str"},
        "cloud_builder_password": {"required": True, "type": "str"},
        "sddc_management_domain_payload": {"required": True, "type": "dict"}
    }
    
    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    cloud_builder_ip = module.params['cloud_builder_ip']
    cloud_builder_user = module.params['cloud_builder_user']
    cloud_builder_password = module.params['cloud_builder_password']
    sddc_management_domain_payload = module.params['sddc_management_domain_payload']
    # if sddc_management_domain_payload is None:
    #     module.fail_json(msg="sddc_management_domain_payload is required")
    # else:
    #     module.exit_json(changed=False, meta=sddc_management_domain_payload)

    try:
        api_client = CloudBuilderApiClient(cloud_builder_ip, cloud_builder_user, cloud_builder_password)
        managment_domain_validation = api_client.validate_sddc(json.dumps(sddc_management_domain_payload))
        payload_data = managment_domain_validation.data
        module.exit_json(changed=False, meta=payload_data)
    except VcfAPIException as e:
        module.fail_json(msg=f"Error: {e}")

if __name__ == '__main__':
    main()