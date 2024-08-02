#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible_collections.vmware.vcf.plugins.module_utils.basic import *
from module_utils.sddc_manager import SddcManagerApiClient
from module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation


class SddcManagerCluster:
    def __init__(self, sddc_manager_ip, sddc_manager_user, sddc_manager_password, sddc_cluster_payload):
        self.sddc_manager_ip = sddc_manager_ip
        self.sddc_manager_user = sddc_manager_user
        self.sddc_manager_password = sddc_manager_password
        self.sddc_cluster_payload = sddc_cluster_payload
        self.api_client = SddcManagerApiClient(self.sddc_manager_ip, self.sddc_manager_user, self.sddc_manager_password)

    def get_cluster_id_by_name(self):
        cluster_name = self.sddc_cluster_payload['clusterName']
        api_response = self.api_client.get_clusters_all_clusters()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == cluster_name:
                return element
        return None

    def validate_clusters(self):
        try:
            api_response = self.api_client.validate_clusters(self.sddc_cluster_payload)
            payload_data = api_response.data
            return {"changed": True, "meta": payload_data}
        except VcfAPIException as e:
            return {"changed": False, "meta": payload_data}

    def validate_datastore_on_cluster(self):
        try:
            api_response = self.api_client.validate_mount_datastore_on_cluster(self.sddc_cluster_payload)
            payload_data = api_response.data
            return {"changed": True, "meta": payload_data}
        except VcfAPIException as e:
            return {"changed": False, "meta": payload_data}

    def create_clusters(self):
        try:
            api_response = self.api_client.create_clusters(self.sddc_cluster_payload)
            payload_data = api_response.data
            return {"changed": True, "meta": payload_data}
        except VcfAPIException as e:
            return {"changed": False, "meta": payload_data}

    def update_cluster(self):
        cluster_id = self.get_cluster_id_by_name()
        if cluster_id is None:
            return {"changed": False, "msg": "Cluster not found"}
        try:
            api_response = self.api_client.update_cluster(cluster_id, self.sddc_cluster_payload)
            payload_data = api_response.data
            return {"changed": True, "meta": payload_data}
        except:
            return {"changed": False, "meta": payload_data}

    def delete_cluster(self):
        cluster_id = self.get_cluster_id_by_name()
        if cluster_id is None:
            return {"changed": False, "msg": "Cluster not found"}
        try:
            api_response = self.api_client.delete_cluster(cluster_id)
            payload_data = api_response.data
            return {"changed": True, "meta": payload_data}
        except:
            return {"changed": False, "meta": payload_data}

    def mount_datastore_on_cluster(self):
        '''
        TO do:
        have to add a check for remote datastores 
        '''
        cluster_id = self.get_cluster_id_by_name()
        if cluster_id is None:
            return {"changed": False, "msg": "Cluster not found"}
        try:
            api_response = self.api_client.mount_datastore_on_cluster(cluster_id, self.sddc_cluster_payload)
            payload_data = api_response.data
            return {"changed": True, "meta": payload_data}
        except:
            return {"changed": False, "meta": payload_data}

    def unmount_datastore_on_cluster(self):
        cluster_id = self.get_cluster_id_by_name()
        if cluster_id is None:
            return {"changed": False, "msg": "Cluster not found"}
        try:
            api_response = self.api_client.unmound_datastore_on_cluster(cluster_id, self.sddc_cluster_payload)
            payload_data = api_response.data
            return {"changed": True, "meta": payload_data}
        except:
            return {"changed": False, "meta": payload_data}

def main():
    parameters = {
        "sddc_manager_ip": {"required": True, "type": "str"},
        "sddc_manager_user": {"required": True, "type": "str"},
        "sddc_manager_password": {"required": True, "type": "str"},
        "sddc_cluster_payload": {"required": False, "type": "dict", "default": None},
        "validate": {"required": False, "type": "bool", "default": False},
        "state": {"required": True, "type": "str", "choices": ['create', 'delete', 'expand', 'compact', 
                                                                'stretch', 'unstretch','mount_datastore', 'unmount_datastore', 'add_remote_datastore']}
    }

    module = AnsibleModule(supports_check_mode=True,
                            argument_spec=parameters)
    
    sddc_manager_ip = module.params['sddc_manager_ip']
    sddc_manager_user = module.params['sddc_manager_user']
    sddc_manager_password = module.params['sddc_manager_password']
    sddc_cluster_payload = module.params['sddc_cluster_payload']
    validate = module.params['validate']
    state = module.params['state']

    sddc_manager_cluster = SddcManagerCluster(sddc_manager_ip, sddc_manager_user, sddc_manager_password, sddc_cluster_payload)

    state_methods = {
        'create': sddc_manager_cluster.create_clusters,
        'delete': sddc_manager_cluster.delete_cluster,
        'expand': sddc_manager_cluster.update_cluster,
        'compact': sddc_manager_cluster.update_cluster,
        'stretch': sddc_manager_cluster.update_cluster,
        'unstretch': sddc_manager_cluster.update_cluster,
        'mount_datastore': sddc_manager_cluster.mount_datastore_on_cluster,
        'unmount_datastore': sddc_manager_cluster.unmount_datastore_on_cluster,
        'add_remote_datastore': sddc_manager_cluster.mount_datastore_on_cluster,
    }

    validate_states = ['create', 'expand', 'compact', 'stretch', 'unstretch', 'mount_datastore', 'unmount_datastore', 'add_remote_datastore']

    if state in state_methods:
        try:
            if validate and state in validate_states:
                return sddc_manager_cluster.validate_clusters() if state != 'mount_datastore' else sddc_manager_cluster.validate_datastore_on_cluster()
            else:
                return state_methods[state]()
        except Exception as e:
            return {"changed": False, "msg": f"Error: {e}"}
    else:
        return {"changed": False, "msg": "Invalid state"}
    # sddc_manager_cluster = SddcManagerCluster(sddc_manager_ip, sddc_manager_user, sddc_manager_password, sddc_cluster_payload)

    # if validate and (state == 'create' or state == 'expand' or state == 'compact' or state == 'stretch' or state == 'unstretch'):
    #     return sddc_manager_cluster.validate_clusters()
    # elif validate and (state == 'mount_datastore' or state == 'unmount_datastore' or state == 'add_remote_datastore'):
    #     return sddc_manager_cluster.validate_datastore_on_cluster()
    # elif state == 'create':
    #     return sddc_manager_cluster.create_clusters()
    # elif state == 'expand' or state == 'compact' or state == 'stretch' or state == 'unstretch':
    #     return sddc_manager_cluster.update_cluster()
    # elif state == 'delete':
    #     return sddc_manager_cluster.delete_cluster()
    # elif state == 'mount_datastore':
    #     return sddc_manager_cluster.mount_datastore_on_cluster()
    # elif state == 'unmount_datastore':
    #     return sddc_manager_cluster.unmount_datastore_on_cluster()
    # else:
    #     return {"changed": False, "msg": "Invalid state"}

if __name__ == '__main__':
    main()