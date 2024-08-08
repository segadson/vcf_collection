#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import basic
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
        "sddc_manager_user": {"required": True, "type": "str"},
        "sddc_manager_password": {"required": True, "type": "str"},
        "cluster_image_name": {"required": True, "type": "str"},
        "state": {"required": True, "type": "str", "choices": ['upload ', 'delete']}
    }

    module = AnsibleModule(supports_check_mode=True,
                           argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    cluster_image_name = module.params['cluster_image_name']
    state = module.params['state']

    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)

    state_methods = {
        'upload': api_client.upload_life_cycle_manager_image,
        'delete': api_client.delete_lifecycle_manager_image,
    }

    if state in state_methods:
        try:
            api_response = state_methods[state](cluster_image_name)
            module.exit_json(changed=True, data=api_response.data)
        except VcfAPIException as e:
            module.fail_json(msg=str(e))
    else:
        module.exit_json(changed=False, meta="Not Valid Action")
    # if state == 'upload':
    #     try:
    #         api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    #         api_response = api_client.upload_life_cycle_manager_image(cluster_image_name)
    #         module.exit_json(changed=True, data=api_response.data)
    #     except VcfAPIException as e:
    #         module.fail_json(msg=str(e))

    # elif state == 'delete':
    #     try:
    #         api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    #         api_response = api_client.delete_lifecycle_manager_image(cluster_image_name)
    #         module.exit_json(changed=True, data=api_response.data)
    #     except VcfAPIException as e:
    #         module.fail_json(msg=str(e))

    # else:
    #     module.exit_json(changed=False, meta="Not Valid Action")
        
        

if __name__ == '__main__':
    main()