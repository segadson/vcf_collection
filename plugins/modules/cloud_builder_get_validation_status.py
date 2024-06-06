#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible.module_utils.basic import *
from module_utils.cloud_builder import CloudBuilderApiClient
from module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation

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

        if payload_data['executionStatus'] == 'FAILED':
            validation_check_list = payload_data['validationChecks']
            error_check_list = []
            for validation_check in validation_check_list:
                if validation_check['resultStatus'] == 'FAILED':
                    error_check_list.append(validation_check)

            module.fail_json(msg=f"Error List: {error_check_list}")
        else:
            module.exit_json(changed=False, meta=payload_data)
    except VcfAPIException as e:
        module.fail_json(msg=f"Error: {e}")

if __name__ == '__main__':
    main()