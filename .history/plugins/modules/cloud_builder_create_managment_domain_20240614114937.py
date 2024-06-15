#!/usr/bin/python
import os
import sys


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
    try:
        api_client = CloudBuilderApiClient(cloud_builder_ip, cloud_builder_user, cloud_builder_password)
        managment_domain_validation = api_client.create_sddc(json.dumps(sddc_management_domain_payload))
        payload_data = managment_domain_validation.data
        module.exit_json(changed=False, meta=payload_data)
    except VcfAPIException as e:
        module.fail_json(msg=f"Error: {e}")

if __name__ == '__main__':
    main()