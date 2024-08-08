from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import os

# Add the directory containing the ansible module to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../../../lib/python3.10/site-packages'))

import json
import pytest
import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes

from ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder import CloudBuilderApiClient
from ansible_collections.vmware.vcf.plugins.module_utils.exceptions import VcfAPIException
from ansible_collections.vmware.vcf.plugins.modules import cloud_builder_create_management_domain



def exit_json(*args, **kwargs):
    raise AnsibleExitJson(kwargs)

def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)

class AnsibleExitJson(Exception):
    pass

class AnsibleFailJson(Exception):
    pass

def set_module_args(args):
    """Prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)

class TestCloudBuilderApiClient(TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    @patch('ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder.CloudBuilderApiClient.create_sddc')
    def test_create_management_domain(self, MockCreateSddc):
        mock_instance = MockCreateSddc.return_value
        mock_instance.create_sddc.return_value = {
            "status_code": 201,
            "message": "Created",
            "data": {
                "id": "26c27804-f837-4e4f-b50f-1625af792f0f",
                "executionStatus": "COMPLETED",
                "validationChecks": [],
                "additionalProperties": {
                    "sddcSpec": "{...}"  # Truncated for brevity
                }
            }
        }
        set_module_args({
            'cloud_builder_ip': 'sfo-cb01.rainpole.local',
            'cloud_builder_user': 'admin',
            'cloud_builder_password': 'VMware1!',
            'sddc_management_domain_payload': {
                "dvSwitchVersion": "7.0.0",
                "skipEsxThumbprintValidation": True,
                "managementPoolName": "bringup-networkpool",
                "sddcManagerSpec": {
                    "hostname": "sfo-vcf01",
                    "ipAddress": "10.0.0.4",
                    "localUserPassword": "xxxxxxxxxxxx",
                    "rootUserCredentials": {
                        "username": "root",
                        "password":"xxxxxxx"
                    },
                    "secondUserCredentials": {
                        "username": "vcf",
                        "password": "xxxxxxx"
                    }
                }
            }
        })

        with self.assertRaises(AnsibleExitJson) as result:
            cloud_builder_create_management_domain.main()
        
        mock_instance.create_sddc.assert_called_once()
        self.assertEqual(result.exception.args[0]['message'], "Created")

if __name__ == '__main__':
    unittest.main()




















'''
{
            'cloud_builder_ip': 'sfo-cb01.rainpole.local',
            'cloud_builder_user': 'admin',
            'cloud_builder_password': 'VMware1!',
            'sddc_management_domain_payload': {
                "dvSwitchVersion": "7.0.0",
                "skipEsxThumbprintValidation": True,
                "managementPoolName": "bringup-networkpool",
                "sddcManagerSpec": {
                    "hostname": "sfo-vcf01",
                    "ipAddress": "10.0.0.4",
                    "localUserPassword": "xxxxxxxxxxxx",
                    "rootUserCredentials": {
                        "username": "root",
                        "password": "xxxxxxx"
                    },
                    "secondUserCredentials": {
                        "username": "vcf",
                        "password": "xxxxxxx"
                    }
                },
                "sddcId": "sddcId-public-api-01",
                "esxLicense": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
                "workflowType": "VCF",
                "ntpServers": ["10.0.0.250"],
                "dnsSpec": {
                    "subdomain": "vrack.vsphere.local",
                    "domain": "vsphere.local",
                    "nameserver": "10.0.0.250",
                    "secondaryNameserver": "10.0.0.251"
                },
                "networkSpecs": [
                    {
                        "subnet": "10.0.0.0/22",
                        "vlanId": "0",
                        "mtu": "1500",
                        "networkType": "MANAGEMENT",
                        "gateway": "10.0.0.250"
                    },
                    {
                        "subnet": "10.0.4.0/24",
                        "includeIpAddressRanges": [
                            {
                                "startIpAddress": "10.0.4.7",
                                "endIpAddress": "10.0.4.48"
                            },
                            {
                                "startIpAddress": "10.0.4.3",
                                "endIpAddress": "10.0.4.6"
                            }
                        ],
                        "includeIpAddress": ["10.0.4.50", "10.0.4.49"],
                        "vlanId": "0",
                        "mtu": "8940",
                        "networkType": "VSAN",
                        "gateway": "10.0.4.253"
                    },
                    {
                        "subnet": "10.0.8.0/24",
                        "includeIpAddressRanges": [
                            {
                                "startIpAddress": "10.0.8.3",
                                "endIpAddress": "10.0.8.50"
                            }
                        ],
                        "vlanId": "0",
                        "mtu": "8940",
                        "networkType": "VMOTION",
                        "gateway": "10.0.8.253"
                    }
                ],
                "nsxtSpec": {
                    "nsxtManagerSize": "medium",
                    "nsxtManagers": [
                        {
                            "hostname": "sfo-m01-nsx01a",
                            "ip": "10.0.0.31"
                        },
                        {
                            "hostname": "sfo-m01-nsx01b",
                            "ip": "10.0.0.32"
                        },
                        {
                            "hostname": "sfo-m01-nsx01c",
                            "ip": "10.0.0.33"
                        }
                    ],
                    "rootNsxtManagerPassword": "xxxxxxx",
                    "nsxtAdminPassword": "xxxxxxx",
                    "nsxtAuditPassword": "xxxxxxx",
                    "vip": "10.0.0.30",
                    "vipFqdn": "sfo-m01-nsx01",
                    "nsxtLicense": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
                    "transportVlanId": 0,
                    "ipAddressPoolSpec": {
                        "name": "sfo01-m01-cl01-tep01",
                        "description": "ESXi Host Overlay TEP IP Pool",
                        "subnets": [
                            {
                                "ipAddressPoolRanges": [
                                    {
                                        "start": "172.16.14.101",
                                        "end": "172.16.14.108"
                                    }
                                ],
                                "cidr": "172.16.14.0/24",
                                "gateway": "172.16.14.1"
                            }
                        ]
                    }
                },
                "vsanSpec": {
                    "licenseFile": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
                    "datastoreName": "sfo-m01-cl01-ds-vsan01",
                    "esaConfig": {
                        "enabled": False
                    }
                },
                "dvsSpecs": [
                    {
                        "mtu": 8940,
                        "niocSpecs": [
                            {
                                "trafficType": "VSAN",
                                "value": "HIGH"
                            },
                            {
                                "trafficType": "VMOTION",
                                "value": "LOW"
                            },
                            {
                                "trafficType": "VDP",
                                "value": "LOW"
                            },
                            {
                                "trafficType": "VIRTUALMACHINE",
                                "value": "HIGH"
                            },
                            {
                                "trafficType": "MANAGEMENT",
                                "value": "NORMAL"
                            },
                            {
                                "trafficType": "NFS",
                                "value": "LOW"
                            },
                            {
                                "trafficType": "HBR",
                                "value": "LOW"
                            },
                            {
                                "trafficType": "FAULTTOLERANCE",
                                "value": "LOW"
                            },
                            {
                                "trafficType": "ISCSI",
                                "value": "LOW"
                            }
                        ],
                        "dvsName": "sfo-m01-cl01-vds01",
                        "vmnicsToUplinks": [
                            {
                                "id": "vmnic0",
                                "uplink": "uplink1"
                            },
                            {
                                "id": "vmnic1",
                                "uplink": "uplink2"
                            }
                        ],
                        "nsxTeamings": [
                            {
                                "policy": "LOADBALANCE_SRCID",
                                "activeUplinks": ["uplink1", "uplink2"],
                                "standByUplinks": []
                            }
                        ],
                        "networks": ["MANAGEMENT", "VSAN", "VMOTION"],
                        "nsxtSwitchConfig": {
                            "transportZones": [
                                {
                                    "name": "sfo-m01-tz-overlay01",
                                    "transportType": "OVERLAY"
                                },
                                {
                                    "name": "sfo-m01-tz-vlan01",
                                    "transportType": "VLAN"
                                }
                            ]
                        }
                    }
                ],
                "clusterSpec": {
                    "clusterName": "sfo-m01-cl01",
                    "clusterEvcMode": "",
                    "resourcePoolSpecs": [
                        {
                            "cpuSharesLevel": "high",
                            "cpuSharesValue": 0,
                            "name": "sfo-m01-cl01-rp-sddc-mgmt",
                            "memorySharesValue": 0,
                            "cpuReservationPercentage": 0,
                            "memoryLimit": -1,
                            "memoryReservationPercentage": 0,
                            "cpuReservationExpandable": True,
                            "memoryReservationExpandable": True,
                            "memorySharesLevel": "normal",
                            "cpuLimit": -1,
                            "type": "management"
                        },
                        {
                            "cpuSharesLevel": "high",
                            "cpuSharesValue": 0,
                            "name": "sfo-m01-cl01-rp-sddc-network",
                            "memorySharesValue": 0,
                            "cpuReservationPercentage": 0,
                            "memoryLimit": -1,
                            "memoryReservationPercentage": 0,
                            "cpuReservationExpandable": True,
                            "memoryReservationExpandable": True,
                            "memorySharesLevel": "normal",
                            "cpuLimit": -1,
                            "type": "network"
                        },
                        {
                            "cpuSharesLevel": "normal",
                            "cpuSharesValue": 0,
                            "name": "sfo-m01-cl01-rp-sddc-compute",
                            "memorySharesValue": 0,
                            "cpuReservationPercentage": 0,
                            "memoryLimit": -1,
                            "memoryReservationPercentage": 0,
                            "cpuReservationExpandable": True,
                            "memoryReservationExpandable": True,
                            "memorySharesLevel": "normal",
                            "cpuLimit": -1,
                            "type": "compute"
                        },
                        {
                            "name": "sfo-m01-cl01-rp-user-compute",
                            "type": "compute",
                            "cpuReservationMhz": 2100,
                            "cpuLimit": -1,
                            "cpuReservationExpandable": True,
                            "cpuSharesLevel": "normal",
                            "memoryReservationMb": 3128,
                            "memoryReservationExpandable": True,
                            "memorySharesLevel": "normal",
                            "memorySharesValue": 0
                        }
                    ]
                },
                "pscSpecs": [
                    {
                        "pscSsoSpec": {
                            "ssoDomain": "vsphere.local"
                        },
                        "adminUserSsoPassword": "xxxxxxx"
                    }
                ],
                "vcenterSpec": {
                    "vcenterIp": "10.0.0.6",
                    "vcenterHostname": "sfo-m01-vc01",
                    "licenseFile": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
                    "rootVcenterPassword": "xxxxxxx",
                    "vmSize": "tiny"
                },
                "hostSpecs": [
                    {
                        "credentials": {
                            "username": "root",
                            "password": "xxxxxxx"
                        },
                        "ipAddressPrivate": {
                            "subnet": "255.255.252.0",
                            "cidr": "",
                            "ipAddress": "10.0.0.100",
                            "gateway": "10.0.0.250"
                        },
                        "hostname": "sfo01-m01-esx01",
                        "association": "sfo-m01-dc01"
                    },
                    {
                        "credentials": {
                            "username": "root",
                            "password": "xxxxxxx"
                        },
                        "ipAddressPrivate": {
                            "subnet": "255.255.252.0",
                            "cidr": "",
                            "ipAddress": "10.0.0.101",
                            "gateway": "10.0.0.250"
                        },
                        "hostname": "sfo01-m01-esx02",
                        "association": "sfo-m01-dc01"
                    },
                    {
                        "credentials": {
                            "username": "root",
                            "password": "xxxxxxx"
                        },
                        "ipAddressPrivate": {
                            "subnet": "255.255.255.0",
                            "cidr": "",
                            "ipAddress": "10.0.0.102",
                            "gateway": "10.0.0.250"
                        },
                        "hostname": "sfo01-m01-esx03",
                        "association": "sfo-m01-dc01"
                    },
                    {
                        "credentials": {
                            "username": "root",
                            "password": "xxxxxxx"
                        },
                        "ipAddressPrivate": {
                            "subnet": "255.255.255.0",
                            "cidr": "",
                            "ipAddress": "10.0.0.103",
                            "gateway": "10.0.0.250"
                        },
                        "hostname": "sfo01-m01-esx04",
                        "association": "sfo-m01-dc01"
                    }
                ]
            }
        }
'''