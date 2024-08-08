#!/usr/bin/python
import os
import sys


# current_dir = os.path.dirname(os.path.realpath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import basic
from ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder import CloudBuilderApiClient
from ansible_collections.vmware.vcf.plugins.module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation
DOCUMENTATION = '''
---
module: cloud_builder_create_management_domain
short_description: This module creates a management domain in Cloud Builder
description:
    - "This module is a wrapper around the Cloud Builder API. It creates a management domain in the SDDC."
author:
    - Your Name (@yourusername)
options:
    cloud_builder_ip:
        description:
            - The IP address of the Cloud Builder.
        required: true
        type: str
    cloud_builder_user:
        description:
            - The username for the Cloud Builder.
        required: true
        type: str
    cloud_builder_password:
        description:
            - The password for the Cloud Builder.
        required: true
        type: str
    sddc_management_domain_payload:
        description:
            - The payload for the management domain.
        required: true
        type: dict
requirements:
    - python >= 3.6
'''

EXAMPLES = '''
# How to use this module in your playbook
- name: Create management domain
  cloud_builder_create_management_domain:
    cloud_builder_ip: "192.168.1.1"
    cloud_builder_user: "admin"
    cloud_builder_password: "password"
    sddc_management_domain_payload: {"key": "value"}
'''

RETURN = '''
management_domain:
    description: The management domain that was created.
    returned: always
    type: dict
'''

def main():
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
    
    # Debugging statement to check parameters
    print(f"Parameters: {module.params}")

    print("Inside Main Function")

    try:
        api_client = CloudBuilderApiClient(cloud_builder_ip, cloud_builder_user, cloud_builder_password)
        result = api_client.create_sddc(json.dumps(sddc_management_domain_payload))
        
        print(f"Result: {result}")
        
        payload_data = result.data
        module.exit_json(changed=False, meta=payload_data)
    
    except VcfAPIException as e:
        module.fail_json(msg=f"Error: {e}")

if __name__ == '__main__':
    main()