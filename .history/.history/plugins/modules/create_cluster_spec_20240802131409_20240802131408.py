#!/usr/bin/python
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ansible_collections.vmware.vcf.plugins.moduleutils.basic import *
from module_utils.sddc_manager import SddcManagerApiClient
from module_utils.exceptions import VcfAPIException
from datetime import datetime
import time
import json
import logging

import yaml

#Todo Documentation

############################################
#To Do Get cluster image ID by name
############################################
def get_cluster_image_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, cluster_image_name):
    cluster_image_id = ""
    pass
    return cluster_image_id

def get_host_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, host_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_all_hosts('UNASSIGNED_USEABLE')
    payload_data = api_response.data
    for element in payload_data['elements']:
        if element['fqdn'] == host_name:
            host_id = element['id']
            return host_id
def get_vsas_provider_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, vsas_provider_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_all_vsas_providers()
    payload_data = api_response.data
    for element in payload_data['elements']: #to do check for elements
        if element['name'] == vsas_provider_name:
            vsas_provider_id = element['id']
            return vsas_provider_id
def get_vsas_provider_user_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, vsas_provider_user_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_all_vsas_provider_users()
    payload_data = api_response.data
    for element in payload_data['elements']: #to do check for elements
        if element['name'] == vsas_provider_user_name:
            vsas_provider_user_id = element['id']
            return vsas_provider_user_id
def get_vsas_provider_storage_container_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, vsas_provider_storage_container_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_all_vsas_provider_storage_containers()
    payload_data = api_response.data
    for element in payload_data['elements']: #to do check for elements
        if element['name'] == vsas_provider_storage_container_name:
            vsas_provider_storage_container = element
            return vsas_provider_storage_container

    #To Do I have to finish the VSAN HCI Remote Datastroe
def get_vsan_datastore_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, vsan_datastore_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_vsan_remote_hci_datastore_from_cluster()
    payload_data = api_response.data
    for element in payload_data['elements']:
        if element['name'] == vsan_datastore_name:
            vsan_datastore_id = element['id']
            return vsan_datastore_id
def get_domain_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, domain_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_all_domains()
    payload_data = api_response.data
    for element in payload_data['elements']:
        if element['name'] == domain_name:
            domain_id = element['id']
            return domain_id

def get_cluster_image_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, cluster_image_name):
    api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
    api_response = api_client.get_all_cluster_images()
    payload_data = api_response.data
    for element in payload_data['elements']:
        if element['name'] == cluster_image_name:
            cluster_image_id = element['id']
            return cluster_image_id
        
def create_cluster_payload(sddc_manager_ip, sddc_manager_user, sddc_manager_password, sddc_cluster_payload):
    '''
    {
        "domainId" : "f36faa4e-de87-49fb-b4f5-1699de159658",
        "computeSpec" : {
        "clusterSpecs" : [ {
            "name" : "sfo-w01-cl02",
            "hostSpecs" : [ {
            "id" : "3e64d6c3-4880-4bbf-8079-4b8493406d01",
            "username" : "root",
            "hostNetworkSpec" : {
                "vmNics" : [ {
                "id" : "vmnic0",
                "vdsName" : "sfo-w01-cl02-vds01",
                "uplink" : "uplink1"
                }, {
                "id" : "vmnic1",
                "vdsName" : "sfo-w01-cl02-vds01",
                "uplink" : "uplink2"
                } ]
            }
            }, {
            "id" : "2b808e97-6681-41f4-b1bf-54dd47ef3720",
            "username" : "root",
            "hostNetworkSpec" : {
                "vmNics" : [ {
                "id" : "vmnic0",
                "vdsName" : "sfo-w01-cl02-vds01",
                "uplink" : "uplink1"
                }, {
                "id" : "vmnic1",
                "vdsName" : "sfo-w01-cl02-vds01",
                "uplink" : "uplink2"
                } ]
            }
            }, {
            "id" : "66e5330a-4d10-4ba3-8616-5caeb2650806",
            "username" : "root",
            "hostNetworkSpec" : {
                "vmNics" : [ {
                "id" : "vmnic0",
                "vdsName" : "sfo-w01-cl02-vds01",
                "uplink" : "uplink1"
                }, {
                "id" : "vmnic1",
                "vdsName" : "sfo-w01-cl02-vds01",
                "uplink" : "uplink2"
                } ]
            }
            } ],
            "datastoreSpec" : {
            "vsanDatastoreSpec" : {
                "failuresToTolerate" : 1,
                "datastoreName" : "sfo-w01-cl02-ds-vsan01"
            }
            },
            "networkSpec" : {
            "vdsSpecs" : [ {
                "name" : "sfo-w01-cl02-vds01",
                "nsxtSwitchConfig" : {
                "transportZones" : [ {
                    "name" : "sfo-w01-nsx-overlay",
                    "transportType" : "OVERLAY"
                }, {
                    "name" : "sfo-w01-nsx-vlan01",
                    "transportType" : "VLAN"
                } ],
                "hostSwitchOperationalMode" : "STANDARD"
                },
                "portGroupSpecs" : [ {
                "name" : "sfo-w01-cl02-vds01-pg-mgmt",
                "transportType" : "MANAGEMENT",
                "activeUplinks" : [ "uplink1", "uplink2" ],
                "teamingPolicy" : "loadbalance_loadbased"
                }, {
                "name" : "sfo-w01-cl02-vds01-pg-vsan",
                "transportType" : "VSAN",
                "activeUplinks" : [ "uplink1", "uplink2" ],
                "teamingPolicy" : "loadbalance_loadbased"
                }, {
                "name" : "sfo-w01-cl02-vds01-pg-vmotion",
                "transportType" : "VMOTION",
                "activeUplinks" : [ "uplink1", "uplink2" ],
                "teamingPolicy" : "loadbalance_loadbased"
                } ],
                "mtu" : 9000
            } ],
            "nsxClusterSpec" : {
                "nsxTClusterSpec" : {
                "uplinkProfiles" : [ {
                    "name" : "Uplink-Profile-1",
                    "teamings" : [ {
                    "policy" : "FAILOVER_ORDER",
                    "activeUplinks" : [ "uplink-1" ],
                    "standByUplinks" : [ "uplink-2" ]
                    } ],
                    "transportVlan" : 2
                } ]
                }
            },
            "networkProfiles" : [ {
                "name" : "sfo-w01-cl02-network-profile01",
                "isDefault" : true,
                "nsxtHostSwitchConfigs" : [ {
                "vdsName" : "sfo-w01-cl02-vds01",
                "uplinkProfileName" : "Uplink-Profile-1",
                "vdsUplinkToNsxUplink" : [ {
                    "vdsUplinkName" : "uplink1",
                    "nsxUplinkName" : "uplink-1"
                }, {
                    "vdsUplinkName" : "uplink2",
                    "nsxUplinkName" : "uplink-2"
                } ]
                } ]
            } ]
            },
            "advancedOptions" : {
            "evcMode" : "",
            "highAvailability" : {
                "enabled" : false
            }
            }
        } ],
        "skipFailedHosts" : false
        },
        "deployWithoutLicenseKeys" : true
    }
    '''
    cluster_payload = {}
    #Get Domain
    domain_id = get_domain_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, sddc_cluster_payload['domain_name'])

    #Create Cluster Spec
    cluster_spec = []

    for cluster in  sddc_cluster_payload:
        cluster_spec_element = {}
        cluster_spec_element['name'] = cluster['name']
        host_specs = []
        for host in cluster['hosts']:
            #Create Host Network Spec
            '''
            {
            "vmNics" : [ {
                "id" : "vmnic0",
                "vdsName" : "sfo-w01-cl01-vds01",
                "uplink" : "uplink1"
            }, {
                "id" : "vmnic1",
                "vdsName" : "sfo-w01-cl01-vds01",
                "uplink" : "uplink2"
            }, {
                "id" : "vmnic2",
                "vdsName" : "sfo-w01-cl01-vds02",
                "uplink" : "uplink1"
            }, {
                "id" : "vmnic3",
                "vdsName" : "sfo-w01-cl01-vds02",
                "uplink" : "uplink2"
            } ]
            }
            '''
            host_network_specs = host['host_network_specs'] 

            host_network_spec_obj = {}
            vm_nics = []
            for vm_nic in host_network_specs['vm_nics']:
                vm_nic_element = {}
                vm_nic_element['id'] = vm_nic['id']
                vm_nic_element['vdsName'] = vm_nic['vds_name']
                vm_nic_element['uplink'] = vm_nic['uplink']
                vm_nics.append(vm_nic_element)
            host_network_spec_obj['vmNics'] = vm_nics

            host_id = get_host_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, host)
            host_spec = {}
            host_spec['id'] = host_id
            host_spec['username'] = host['username']
            host_spec['hostNetworkSpec'] = host_network_spec_obj
            host_specs.append(host_spec)
        

        #Create Datastore Spec
        datastore_spec = {}
        if cluster['datastore_type'] == 'vsan':
            vsan_datastore_spec = {}
            vsan_datastore_spec['failuresToTolerate'] = cluster['failuresToTolerate']
            vsan_datastore_spec['licenseKey'] = cluster['licenseKey']
            vsan_datastore_spec['datastoreName'] = cluster['datastoreName']
            vsan_datastore_spec['esaConfig'] = cluster['esaConfig']
            datastore_spec['vsanDatastoreSpec'] = vsan_datastore_spec
            cluster_spec_element['datastoreSpec'] = datastore_spec
        elif cluster['datastore_type'] == 'vvol':
            vvol_datastore_specs =  []
            for data_store in cluster['datastores']:
                vvol_datastore = {}
                vvol_datastore['datastoreName'] = data_store['name']
                #VASA Provider Spec
                vasa_provider_spec = {}
                vasa_provider_spec['vsasProviderId'] = get_vsas_provider_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, cluster['vsasProviderName'])
                vasa_provider_spec['vsasProviderUserId'] = get_vsas_provider_user_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, cluster['vsasProviderUserName'])
                vasa_provider_spec['vsasProviderStorageContainer'] = get_vsas_provider_storage_container_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, cluster['vsasProviderStorageContainerName'])
                vvol_datastore['vasaProviderSpec'] = vasa_provider_spec
                vvol_datastore_specs.append(vvol_datastore)

            datastore_spec['vvolDatastoreSpecs'] = vvol_datastore_specs
            cluster_spec_element['datastoreSpec'] = datastore_spec
        elif cluster['datastore_type'] == 'vmfs':
            '''
            {
            "vmfsDatastoreSpec" : {
                "fcSpec" : [ {
                "datastoreName" : "sfo-w01-cl01-ds-fc01"
                } ]
            }
            }
            '''
            for datastore in cluster['datastores']:
                vmfs_datastore_spec = {}
                fc_spec = []
                for fc_datastore in datastore['fcDatastore']:
                    fc_datastore_spec = {}
                    fc_datastore_spec['datastoreName'] = fc_datastore['name']
                    fc_spec.append(fc_datastore_spec)
                vmfs_datastore_spec['fcSpec'] = fc_spec

            datastore_spec['vmfsDatastoreSpec'] = vmfs_datastore_spec
        elif cluster['datastore_type'] == 'nfs':
            '''
            {
                "nfsDatastoreSpecs" : [ {
                "nasVolume" : {
                    "serverName" : [ "10.0.0.250" ],
                    "path" : "/nfs_mount/my_read_write_folder",
                    "readOnly" : false
                },
                "datastoreName" : "sfo-w01-cl01-ds-nfs01"
                } ]
            }
            '''
            for datastore in cluster['datastores']:
                nfs_datastore_spec = []
                for nfs_datastore in datastore['nfsDatastores']:
                    nfs_datastore_spec_element = {}
                    nas_volume = {}
                    nas_volume['serverName'] = nfs_datastore['serverName']
                    nas_volume['path'] = nfs_datastore['path']
                    nas_volume['readOnly'] = nfs_datastore['readOnly']
                    nfs_datastore_spec_element['nasVolume'] = nas_volume
                    nfs_datastore_spec_element['datastoreName'] = nfs_datastore['name']
                    nfs_datastore_spec.append(nfs_datastore_spec_element)
            datastore_spec['nfsDatastoreSpecs'] = nfs_datastore_spec

        elif cluster['datastore_type'] == 'vsan_hci':
            '''
            {
            "vsanRemoteDatastoreClusterSpec" : {
                "vsanRemoteDatastoreSpec" : [ {
                "datastoreUuid" : "c83f081533b449e1-a1673ed0afdcc7d9"
                } ]
            }
            }
            '''
            vsan_remote_datastore_cluster_spec = {}
            for datastore in cluster['datastores']:
                vsan_remote_datastore_spec = []
                for vsan_datastore in datastore['vsanDatastores']:
                    vsan_remote_datastore_name = vsan_datastore['name']
                    vsan_datastore_id = get_vsan_datastore_id_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, vsan_remote_datastore_name)
                    vsan_remote_datastore_spec_element = {}
                    vsan_remote_datastore_spec_element['datastoreUuid'] = vsan_datastore_id
                    vsan_remote_datastore_spec.append(vsan_remote_datastore_spec_element)
            datastore_spec['vsanRemoteDatastoreSpec'] = vsan_remote_datastore_spec
        else:
            raise VcfAPIException("Invalid Datastore Type")


        #Create Network Spec
        network_spec = {}
        '''
        1) Have to Create a VDS Speck
        2) Have to have a choice of consolidated nsxt spec or individual nsxt spec
         - if consolidated nsxt spec then have to get the nsxt ip address pool name 
        '''

        #Create VDS Config
        """
        [ {
        "name" : "sfo-w01-cl01-vds01",
        "portGroupSpecs" : [ {
            "name" : "sfo-w01-cl01-vds01-pg-mgmt",
            "transportType" : "MANAGEMENT",
            "activeUplinks" : [ "uplink1", "uplink2" ],
            "teamingPolicy" : "loadbalance_ip"
        }, {
            "name" : "sfo-w01-cl01-vds01-pg-vsan",
            "transportType" : "VSAN",
            "activeUplinks" : [ "uplink1" ],
            "standByUplinks" : [ "uplink2" ],
            "teamingPolicy" : "loadbalance_loadbased"
        }, {
            "name" : "sfo-w01-cl01-vds01-pg-vmotion",
            "transportType" : "VMOTION",
            "activeUplinks" : [ "uplink2" ],
            "standByUplinks" : [ "uplink1" ],
            "teamingPolicy" : "loadbalance_srcmac"
        } ],
        "mtu" : 9000
        }, {
        "name" : "sfo-w01-cl01-vds02",
        "nsxtSwitchConfig" : {
            "transportZones" : [ {
            "name" : "sfo-w01-nsx-overlay",
            "transportType" : "OVERLAY"
            }, {
            "name" : "sfo-w01-nsx-vlan01",
            "transportType" : "VLAN"
            } ],
            "hostSwitchOperationalMode" : "STANDARD"
        },
        "mtu" : 9000
        } ]
        """
        vds_spec = []
        for vds in cluster['network_spec']['vds']:
            vds_spec_element = {}
            vds_spec_element['name'] = vds['name']
            port_group_specs = []
            for port_group in vds['portGroups']:
                port_group_spec = {}
                port_group_spec['name'] = port_group['name']
                port_group_spec['transportType'] = port_group['transport_type']
                port_group_spec['activeUplinks'] = port_group['active_uplinks']
                port_group_spec['teamingPolicy'] = port_group['teaming_policy']
                port_group_specs.append(port_group_spec)
            vds_spec_element['portGroupSpecs'] = port_group_specs
            vds_spec_element['mtu'] = vds['mtu']
            
            if cluster['nsxt_switch_config']['nsx_managed'] == True:
                nsxt_switch_config_obj = {}
                nsxt_switch_config_obj['name'] = vds['nsxt_switch_config']['name']

                nsxt_switch_config = {}
                nsxt_switch_config_transport_zones = []
                for transport_zone in vds['nsxt_switch_config']['transportZones']:
                    transport_zone_element = {}
                    transport_zone_element['name'] = transport_zone['name']
                    transport_zone_element['transportType'] = transport_zone['transport_type']
                    nsxt_switch_config_transport_zones.append(transport_zone_element)
                nsxt_switch_config['transportZones'] = nsxt_switch_config_transport_zones
                nsxt_switch_config['hostSwitchOperationalMode'] = vds['nsxt_switch_config']['host_switch_operationalMode']
                vds_spec_element['nsxtSwitchConfig'] = nsxt_switch_config
            if cluster['network_spec']['nsxt_cluster_uplink_spec']['ip_static_ip_pool']:
                '''
                    {
                    "nsxTClusterSpec" : {
                        "ipAddressPoolsSpec" : [ {
                        "name" : "static-ip-pool-01",
                        "subnets" : [ {
                            "ipAddressPoolRanges" : [ {
                            "start" : "10.0.11.50",
                            "end" : "10.0.11.70"
                            }, {
                            "start" : "10.0.11.80",
                            "end" : "10.0.11.150"
                            } ],
                            "cidr" : "10.0.11.0/24",
                            "gateway" : "10.0.11.250"
                        } ]
                        } ],
                        "uplinkProfiles" : [ {
                        "name" : "Uplink-Profile-1",
                        "teamings" : [ {
                            "policy" : "FAILOVER_ORDER",
                            "activeUplinks" : [ "uplink-1" ],
                            "standByUplinks" : [ "uplink-2" ]
                        } ],
                        "transportVlan" : 2
                        } ]
                    }
                    }                
                '''
                nsxt_cluster_uplink_spec = {}
                ip_pool_spec = []
                for ip_pool in cluster['network_spec']['nsxt_cluster_uplink_spec']['ip_static_ip_pool']:
                    ip_pool_element = {}
                    ip_pool_element['name'] = ip_pool['name']
                    subnets = []
                    for subnet in ip_pool['subnets']:
                        subnet_element = {}
                        ip_address_pool_ranges = []
                        for ip_address_pool_range in subnet['ip_address_pool_ranges']:
                            ip_address_pool_range_element = {}
                            ip_address_pool_range_element['start'] = ip_address_pool_range['start']
                            ip_address_pool_range_element['end'] = ip_address_pool_range['end']
                            ip_address_pool_ranges.append(ip_address_pool_range_element)
                        subnet_element['ipAddressPoolRanges'] = ip_address_pool_ranges
                        subnet_element['cidr'] = subnet['cidr']
                        subnet_element['gateway'] = subnet['gateway']
                        subnets.append(subnet_element)
                    ip_pool_element['subnets'] = subnets
                    ip_pool_spec.append(ip_pool_element)
                nsxt_cluster_uplink_spec['ipAddressPoolsSpec'] = ip_pool_spec
                uplink_profiles = []
                for uplink_profile in cluster['network_spec']['nsxt_cluster_uplink_spec']['uplink_profiles']:
                    uplink_profile_element = {}
                    uplink_profile_element['name'] = uplink_profile['name']
                    teamings = []
                    for teaming in uplink_profile['teamings']:
                        teaming_element = {}
                        teaming_element['policy'] = teaming['policy']
                        teaming_element['activeUplinks'] = teaming['active_uplinks']
                        teaming_element['standByUplinks'] = teaming['stand_by_uplinks']
                        teamings.append(teaming_element)
                    uplink_profile_element['teamings'] = teamings
                    uplink_profile_element['transportVlan'] = uplink_profile['transport_vlan']
                    uplink_profiles.append(uplink_profile_element)
                nsxt_cluster_uplink_spec['uplinkProfiles'] = uplink_profiles
                
            if cluster['network_spec']['nsxt_cluster_uplink_spec']['consolidated_nsxt'] == True:
                '''
                {
                "nsxTClusterSpec" : {
                    "ipAddressPoolsSpec" : [ {
                    "name" : "static-ip-pool-01"
                    } ],
                    "uplinkProfiles" : [ {
                    "name" : "Uplink-Profile-1",
                    "teamings" : [ {
                        "policy" : "FAILOVER_ORDER",
                        "activeUplinks" : [ "uplink-1" ],
                        "standByUplinks" : [ "uplink-2" ]
                    } ],
                    "transportVlan" : 2
                    } ]
                }
                }
                '''
                nsxt_cluster_uplink_spec = {}
                ip_pool_spec = []
                for ip_pool in cluster['network_spec']['nsxt_cluster_uplink_spec']['ip_static_ip_pool']:
                    ip_pool_element = {}
                    ip_pool_element['name'] = ip_pool['name']
                    ip_pool_spec.append(ip_pool_element)
                nsxt_cluster_uplink_spec['ipAddressPoolsSpec'] = ip_pool_spec
                uplink_profiles = []
                for uplink_profile in cluster['network_spec']['nsxt_cluster_uplink_spec']['uplink_profiles']:
                    uplink_profile_element = {}
                    uplink_profile_element['name'] = uplink_profile['name']
                    teamings = []
                    for teaming in uplink_profile['teamings']:
                        teaming_element = {}
                        teaming_element['policy'] = teaming['policy']
                        teaming_element['activeUplinks'] = teaming['active_uplinks']
                        teaming_element['standByUplinks'] = teaming['stand_by_uplinks']
                        teamings.append(teaming_element)
                    uplink_profile_element['teamings'] = teamings
                    uplink_profile_element['transportVlan'] = uplink_profile['transport_vlan']
                    uplink_profiles.append(uplink_profile_element)
                nsxt_cluster_uplink_spec['uplinkProfiles'] = uplink_profiles

            
            if cluster['nsxt_switch_config']['nsx_managed'] == True:
                '''
                [ {
                    "name" : "Cluster-1-network-profile01",
                    "isDefault" : true,
                    "nsxtHostSwitchConfigs" : [ {
                    "vdsName" : "sfo-w01-cl01-vds02",
                    "uplinkProfileName" : "Uplink-Profile-1",
                    "ipAddressPoolName" : "static-ip-pool-01",
                    "vdsUplinkToNsxUplink" : [ {
                        "vdsUplinkName" : "uplink1",
                        "nsxUplinkName" : "uplink-1"
                    }, {
                        "vdsUplinkName" : "uplink2",
                        "nsxUplinkName" : "uplink-2"
                    } ]
                    } ]
                } ]
                '''
                #create network profiles
                nsx_network_profiles = []
                for network_profile in cluster['network_spec']['network_profiles']:
                    nsx_network_profile = {}
                    nsx_network_profile['name'] = network_profile['name']
                    nsx_network_profile['isDefault'] = network_profile['is_default']
                    nsxt_host_switch_configs = []
                    for nsxt_host_switch_config in network_profile['nsxt_host_switch_configs']:
                        nsxt_host_switch_config_element = {}
                        nsxt_host_switch_config_element['vdsName'] = nsxt_host_switch_config['vds_name']
                        nsxt_host_switch_config_element['uplinkProfileName'] = nsxt_host_switch_config['uplink_profile_name']
                        nsxt_host_switch_config_element['ipAddressPoolName'] = nsxt_host_switch_config['ip_address_pool_name']
                        vds_uplink_to_nsx_uplink = []
                        for vds_uplink in nsxt_host_switch_config['vds_uplink_to_nsx_uplink']:
                            vds_uplink_element = {}
                            vds_uplink_element['vdsUplinkName'] = vds_uplink['vds_uplink_name']
                            vds_uplink_element['nsxUplinkName'] = vds_uplink['nsx_uplink_name']
                            vds_uplink_to_nsx_uplink.append(vds_uplink_element)
                        nsxt_host_switch_config_element['vdsUplinkToNsxUplink'] = vds_uplink_to_nsx_uplink
                        nsxt_host_switch_configs.append(nsxt_host_switch_config_element)
                    nsx_network_profile['nsxtHostSwitchConfigs'] = nsxt_host_switch_configs
                    nsx_network_profiles.append(nsx_network_profile)
                network_spec['networkProfiles'] = nsx_network_profiles
            vds_spec.append(vds_spec_element)

        cluster_spec_element['networkSpec'] = network_spec
        cluster_spec.append(cluster_spec_element)
    
    #Create Compute Spec
    compute_spec = {}
    compute_spec['clusterSpecs'] = cluster_spec

    #Cluster Advanced Options
    '''
    {
          "evcMode" : "",
          "highAvailability" : {
            "enabled" : false
          }
        }
    '''
    if sddc_cluster_payload['evc_mode']:
        evc_mode = sddc_cluster_payload['evc_mode']
    else:
        evc_mode = ""

    if sddc_cluster_payload['enabled']:
        enabled = sddc_cluster_payload['enabled']
    else:
        enabled = False
    advanced_options = {"evcMode" : evc_mode,
          "highAvailability" : {
            "enabled" : enabled
          }
        }

    #Payload
    cluster_payload['domainId'] = domain_id
    cluster_payload['datastoreSpec'] = datastore_spec
    cluster_payload['hostSpecs'] = host_specs
    cluster_payload['computeSpec'] = compute_spec
    cluster_payload['advancedOptions'] = advanced_options

    if sddc_cluster_payload['cluster_image']:
        cluster_image_id = get_cluster_image_by_name(sddc_manager_ip, sddc_manager_user, sddc_manager_password, sddc_cluster_payload['cluster_image'])
        if cluster_image_id is None:
            raise VcfAPIException("Cluster Image Not Found")
        cluster_payload['clusterImageId'] = cluster_image_id
    return cluster_payload
