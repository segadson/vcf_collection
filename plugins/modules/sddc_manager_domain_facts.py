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
    domain_name=dict(type='str', required=True),
)

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    domain_name = module.params['domain_name']

    

    def get_domain_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, name):
        try:
            api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
            api_response = api_client.get_all_domains()
            payload_data = api_response.data
            for element in payload_data['elements']:
                if element['name'] == name:
                    return element
        except Exception as e:
            module.fail_json(msg="Failed to get host by name: " + str(e))

    domain = get_domain_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, domain_name)

    if domain is None:
        module.fail_json(msg="Domain not found")
    else:
        module.exit_json(changed=False, meta=domain)
if __name__ == '__main__':
    main()

