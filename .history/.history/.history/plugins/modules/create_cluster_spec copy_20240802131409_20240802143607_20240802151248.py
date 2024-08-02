#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible.module_utils import basic
from module_utils.sddc_manager import SddcManagerApiClient
from module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation

'''
MAKE THIS A CLASS


'''

############################################
#To Do Get cluster image ID by name
############################################
class ClusterSpecCreator:
    def __init__(self, sddc_manager_ip, sddc_manager_user, sddc_manager_password):
        self.sddc_manager_ip = sddc_manager_ip
        self.sddc_manager_user = sddc_manager_user
        self.sddc_manager_password = sddc_manager_password
        self.api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)

    def get_cluster_image_id_by_name(self, cluster_image_name):
        cluster_image_id = ""
        # TODO: Implement the logic to get cluster image ID by name
        return cluster_image_id

    def get_host_id_by_name(self, host_name):
        api_response = self.api_client.get_all_hosts('UNASSIGNED_USEABLE')
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['fqdn'] == host_name:
                host_id = element['id']
                return host_id

    def get_vsas_provider_id_by_name(self, vsas_provider_name):
        api_response = self.api_client.get_all_vsas_providers()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == vsas_provider_name:
                vsas_provider_id = element['id']
                return vsas_provider_id

    def get_vsas_provider_user_id_by_name(self, vsas_provider_user_name):
        api_response = self.api_client.get_all_vsas_provider_users()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == vsas_provider_user_name:
                vsas_provider_user_id = element['id']
                return vsas_provider_user_id

    def get_vsas_provider_storage_container_by_name(self, vsas_provider_storage_container_name):
        api_response = self.api_client.get_all_vsas_provider_storage_containers()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == vsas_provider_storage_container_name:
                vsas_provider_storage_container = element
                return vsas_provider_storage_container

    def get_vsan_datastore_id_by_name(self, vsan_datastore_name):
        api_response = self.api_client.get_vsan_remote_hci_datastore_from_cluster()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == vsan_datastore_name:
                vsan_datastore_id = element['id']
                return vsan_datastore_id

    def get_domain_id_by_name(self, domain_name):
        api_response = self.api_client.get_all_domains()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == domain_name:
                domain_id = element['id']
                return domain_id

    def get_cluster_image_by_name(self, cluster_image_name):
        api_response = self.api_client.get_all_cluster_images()
        payload_data = api_response.data
        for element in payload_data['elements']:
            if element['name'] == cluster_image_name:
                cluster_image_id = element['id']
                return cluster_image_id

    def two_pnic_nsx_ip_pool_vsan(self, domain_id, workload_domain_name, cluster_name, hosts):
        host_spec = []
        for host in hosts:
            host_spec.append(self.create_two_host_spec(workload_domain_name, cluster_name, host['id']))
        payload = {
            "domainId": f"{domain_id}",
            "computeSpec": {
                "clusterSpecs": [{
                    "name": f"{workload_domain_name}-{cluster_name}",
                    "hostSpecs": [hosts],
                    "datastoreSpec": {
                        "vsanDatastoreSpec": {
                            "failuresToTolerate": 1,
                            "datastoreName": f"{workload_domain_name}-{cluster_name}-ds-vsan01"
                        }
                    },
                    "networkSpec": {
                        "vdsSpecs": [{
                            "name": f"{workload_domain_name}-{cluster_name}-vds01",
                            "nsxtSwitchConfig": {
                                "transportZones": [{
                                    "name": f"{workload_domain_name}-nsx-overlay",
                                    "transportType": "OVERLAY"
                                }, {
                                    "name": f"{workload_domain_name}-nsx-vlan01",
                                    "transportType": "VLAN"
                                }],
                                "hostSwitchOperationalMode": "STANDARD"
                            },
                            "portGroupSpecs": [{
                                "name": f"{workload_domain_name}-{cluster_name}-vds01-pg-mgmt",
                                "transportType": "MANAGEMENT",
                                "activeUplinks": ["uplink1", "uplink2"],
                                "teamingPolicy": "loadbalance_loadbased"
                            }, {
                                "name": f"{workload_domain_name}-{cluster_name}-vds01-pg-vsan",
                                "transportType": "VSAN",
                                "activeUplinks": ["uplink1", "uplink2"],
                                "teamingPolicy": "loadbalance_loadbased"
                            }, {
                                "name": f"{workload_domain_name}-{cluster_name}-vds01-pg-vmotion",
                                "transportType": "VMOTION",
                                "activeUplinks": ["uplink1", "uplink2"],
                                "teamingPolicy": "loadbalance_loadbased"
                            }],
                            "mtu": 9000
                        }],
                        "nsxClusterSpec": {
                            "nsxTClusterSpec": {
                                "uplinkProfiles": [{
                                    "name": "Uplink-Profile-1",
                                    "teamings": [{
                                        "policy": "FAILOVER_ORDER",
                                        "activeUplinks": ["uplink-1"],
                                        "standByUplinks": ["uplink-2"]
                                    }],
                                    "transportVlan": 2
                                }]
                            }
                        },
                        "networkProfiles": [{
                            "name": f"{workload_domain_name}-{cluster_name}-network-profile01",
                            "isDefault": True,
                            "nsxtHostSwitchConfigs": [{
                                "vdsName": f"{workload_domain_name}-{cluster_name}-vds01",
                                "uplinkProfileName": "Uplink-Profile-1",
                                "vdsUplinkToNsxUplink": [{
                                    "vdsUplinkName": "uplink1",
                                    "nsxUplinkName": "uplink-1"
                                }, {
                                    "vdsUplinkName": "uplink2",
                                    "nsxUplinkName": "uplink-2"
                                }]
                            }]
                        }]
                    },
                    "advancedOptions": {
                        "evcMode": "",
                        "highAvailability": {
                            "enabled": False
                        }
                    }
                }],
                "skipFailedHosts": False
            },
            "deployWithoutLicenseKeys": True
        }
        return payload

    def create_two_host_spec(self, workload_domain_name, cluster_name, host_name):
        # get host id
        host_name = ClusterSpecCreator.get_host_id_by_name(host_name)
        payload = {
            "id": f"{host_name}",
            "username": "root",
            "hostNetworkSpec": {
                "vmNics": [{
                    "id": "vmnic0",
                    "vdsName": f"{workload_domain_name}-{cluster_name}-vds01",
                    "uplink": "uplink1"
                }, {
                    "id": "vmnic1",
                    "vdsName": f"{workload_domain_name}-{cluster_name}-vds01",
                    "uplink": "uplink2"
                }]
            }
        }
        return payload