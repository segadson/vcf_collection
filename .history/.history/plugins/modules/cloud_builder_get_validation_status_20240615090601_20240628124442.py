#!/usr/bin/python
import os
import sys
6


# current_dir = os.path.dirname(os.path.realpath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

from ansible.module_utils.basic import *
from ansible.module_utils.cloud_builder import CloudBuilderApiClient
from ansible.module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation
DOCUMENTATION = '''
---
module: cloud_builder_get_validation_status
short_description: This module checks the validation status of the SDDC in Cloud Builder
description:
    - "This module is a wrapper around the Cloud Builder API. It retrieves the validation status of the SDDC."
author:
    - Your Name (@yourusername)
options:
    cloud_builder_ip:
        description:
            - The IP address of the Cloud Builder.
        required: true
        type: str
    sddc_id:
        description:
            - The ID of the SDDC.
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
requirements:
    - python >= 3.6
'''

EXAMPLES = '''
# How to use this module in your playbook
- name: Get SDDC validation status
  cloud_builder_get_validation_status:
    cloud_builder_ip: "192.168.1.1"
    sddc_id: "sddc1"
    cloud_builder_user: "admin"
    cloud_builder_password: "password"
'''

RETURN = '''
status:
    description: The validation status of the SDDC.
    returned: always
    type: str
validation_checks:
    description: The validation checks performed during the validation of the SDDC.
    returned: when status is 'FAILED'
    type: list
'''
def main():
    parameters = {
        "cloud_builder_ip": {"required": True, "type": "str"},
        "sddc_id": {"required": True, "type": "str"},
        "cloud_builder_user": {"required": True, "type": "str"},
        "cloud_builder_password": {"required": True, "type": "str"}
    }

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    cloud_builder_ip = module.params['cloud_builder_ip']
    sddc_id = module.params['sddc_id']
    cloud_builder_user = module.params['cloud_builder_user']
    cloud_builder_password = module.params['cloud_builder_password']

    try:
        api_client = CloudBuilderApiClient(cloud_builder_ip, cloud_builder_user, cloud_builder_password)
        validation_report = api_client.get_sddc_validation(sddc_id)
        payload_data = validation_report.data
        module.log(msg=payload_data['executionStatus'] )
        if payload_data['executionStatus'] == 'FAILED':
            validation_check_list = payload_data['validationChecks']
            error_check_list = []
            for validation_check in validation_check_list:
                if validation_check['resultStatus'] == 'FAILED':
                    error_check_list.append(validation_check)

            module.fail_json(changed=False, meta=payload_data)
        else:
            module.exit_json(changed=False, meta=payload_data)
    except VcfAPIException as e:
        module.fail_json(changed=False, meta=payload_data)

if __name__ == '__main__':
    main()