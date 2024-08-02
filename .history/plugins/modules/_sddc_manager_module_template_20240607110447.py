#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible.module_utils.basic import *
from module_utils.sddc_manager import SddcManagerApiClient
from module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation

def main():
    parameters = {
        "sddc_manager_ip": {"required": True, "type": "str"},
        "sddc_id": {"required": True, "type": "str"},
        "sddc_manager_user": {"required": True, "type": "str"},
        "sddc_manager_password": {"required": True, "type": "str"}
    }

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_id = module.params['sddc_id']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']

    try:
        api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
        api_response = api_client.get_sddc_domains()
        payload_data = api_response.data
        module.exit_json(changed=False, meta=payload_data)
    except VcfAPIException as e:
        module.fail_json(msg=f"Error: {e}")

if __name__ == '__main__':
    main()