import json
import pytest
from unittest.mock import MagicMock, patch
from ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder import CloudBuilderApiClient
from ansible_collections.vmware.vcf.plugins.module_utils.exceptions import VcfAPIException
from ansible.modules.cloud_builder_create_management_domain import cloud_builder_create_managment_domain
from ansible_collections.vmware.vcf.plugins.module_utils import basic
from ansible_collections.vmware.vcf.plugins.module_utils.common.text.converters import to_bytes

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type




class ModuleFailException(Exception):
    def __init__(self, msg, **kwargs):
        super(ModuleFailException, self).__init__(msg)
        self.fail_msg = msg
        self.fail_kwargs = kwargs


def get_module_mock():
    def f(msg, **kwargs):
        raise ModuleFailException(msg, **kwargs)

    module = MagicMock()
    module.fail_json = f
    module.from_json = json.loads
    return module


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


class TestCloudBuilderApiClient:
    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            cloud_builder_create_managment_domain.main()

    def test_create_management_domain(self):
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
        })

        with patch.object(CloudBuilderApiClient, 'create_sddc') as mock_create_sddc:
            mock_create_sddc.return_value = {
            "status_code": 201,
            "message": "Created",
            "data": {
                "id": "26c27804-f837-4e4f-b50f-1625af792f0f",
                "executionStatus": "COMPLETED",
                "validationChecks": [],
                "additionalProperties": {
                "sddcSpec": "{\n  \"dvSwitchVersion\": \"7.0.0\",\n  \"skipEsxThumbprintValidation\": true,\n  \"managementPoolName\": \"bringup-networkpool\",\n  \"sddcManagerSpec\": {\n    \"hostname\": \"sfo-vcf01\",\n    \"ipAddress\": \"10.0.0.4\",\n    \"localUserPassword\": \"xxxxxxxxxxxx\",\n    \"rootUserCredentials\": {\n      \"username\": \"root\",\n      \"password\": \"xxxxxxx\"\n    },\n    \"secondUserCredentials\": {\n      \"username\": \"vcf\",\n      \"password\": \"xxxxxxx\"\n    }\n  },\n  \"sddcId\": \"sddcId-public-api-01\",\n  \"esxLicense\": \"XXXXX-XXXXX-XXXXX-XXXXX-XXXXX\",\n  \"workflowType\": \"VCF\",\n  \"ntpServers\": [\n    \"10.0.0.250\"\n  ],\n  \"dnsSpec\": {\n    \"subdomain\": \"vrack.vsphere.local\",\n    \"domain\": \"vsphere.local\",\n    \"nameserver\": \"10.0.0.250\",\n    \"secondaryNameserver\": \"10.0.0.251\"\n  },\n  \"networkSpecs\": [\n    {\n      \"subnet\": \"10.0.0.0/22\",\n      \"vlanId\": \"0\",\n      \"mtu\": \"1500\",\n      \"networkType\": \"MANAGEMENT\",\n      \"gateway\": \"10.0.0.250\"\n    },\n    {\n      \"subnet\": \"10.0.4.0/24\",\n      \"includeIpAddressRanges\": [\n        {\n          \"startIpAddress\": \"10.0.4.7\",\n          \"endIpAddress\": \"10.0.4.48\"\n        },\n        {\n          \"startIpAddress\": \"10.0.4.3\",\n          \"endIpAddress\": \"10.0.4.6\"\n        }\n      ],\n      \"includeIpAddress\": [\n        \"10.0.4.50\",\n        \"10.0.4.49\"\n      ],\n      \"vlanId\": \"0\",\n      \"mtu\": \"8940\",\n      \"networkType\": \"VSAN\",\n      \"gateway\": \"10.0.4.253\"\n    },\n    {\n      \"subnet\": \"10.0.8.0/24\",\n      \"includeIpAddressRanges\": [\n        {\n          \"startIpAddress\": \"10.0.8.3\",\n          \"endIpAddress\": \"10.0.8.50\"\n        }\n      ],\n      \"vlanId\": \"0\",\n      \"mtu\": \"8940\",\n      \"networkType\": \"VMOTION\",\n      \"gateway\": \"10.0.8.253\"\n    }\n  ],\n  \"nsxtSpec\": {\n    \"nsxtManagerSize\": \"medium\",\n    \"nsxtManagers\": [\n      {\n        \"hostname\": \"sfo-m01-nsx01a\",\n        \"ip\": \"10.0.0.31\"\n      },\n      {\n        \"hostname\": \"sfo-m01-nsx01b\",\n        \"ip\": \"10.0.0.32\"\n      },\n      {\n        \"hostname\": \"sfo-m01-nsx01c\",\n        \"ip\": \"10.0.0.33\"\n      }\n    ],\n    \"rootNsxtManagerPassword\": \"xxxxxxx\",\n    \"nsxtAdminPassword\": \"xxxxxxx\",\n    \"nsxtAuditPassword\": \"xxxxxxx\",\n    \"vip\": \"10.0.0.30\",\n    \"vipFqdn\": \"sfo-m01-nsx01\",\n    \"nsxtLicense\": \"XXXXX-XXXXX-XXXXX-XXXXX-XXXXX\",\n    \"transportVlanId\": 0,\n    \"ipAddressPoolSpec\": {\n      \"name\": \"sfo01-m01-cl01-tep01\",\n      \"description\": \"ESXi Host Overlay TEP IP Pool\",\n      \"subnets\": [\n        {\n          \"ipAddressPoolRanges\": [\n            {\n              \"start\": \"172.16.14.101\",\n              \"end\": \"172.16.14.108\"\n            }\n          ],\n          \"cidr\": \"172.16.14.0/24\",\n          \"gateway\": \"172.16.14.1\"\n        }\n      ]\n    }\n  },\n  \"vsanSpec\": {\n    \"licenseFile\": \"XXXXX-XXXXX-XXXXX-XXXXX-XXXXX\",\n    \"datastoreName\": \"sfo-m01-cl01-ds-vsan01\",\n    \"esaConfig\": {\n      \"enabled\": false\n    }\n  },\n  \"dvsSpecs\": [\n    {\n      \"mtu\": 8940,\n      \"niocSpecs\": [\n        {\n          \"trafficType\": \"VSAN\",\n          \"value\": \"HIGH\"\n        },\n        {\n          \"trafficType\": \"VMOTION\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"VDP\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"VIRTUALMACHINE\",\n          \"value\": \"HIGH\"\n        },\n        {\n          \"trafficType\": \"MANAGEMENT\",\n          \"value\": \"NORMAL\"\n        },\n        {\n          \"trafficType\": \"NFS\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"HBR\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"FAULTTOLERANCE\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"ISCSI\",\n          \"value\": \"LOW\"\n        }\n      ],\n      \"dvsName\": \"sfo-m01-cl01-vds01\",\n      \"vmnicsToUplinks\": [\n        {\n          \"id\": \"vmnic0\",\n          \"uplink\": \"uplink1\"\n        },\n        {\n          \"id\": \"vmnic1\",\n          \"uplink\": \"uplink2\"\n        }\n      ],\n      \"nsxTeamings\": [\n        {\n          \"policy\": \"LOADBALANCE_SRCID\",\n          \"activeUplinks\": [\n            \"uplink1\",\n            \"uplink2\"\n          ],\n          \"standByUplinks\": []\n        }\n      ],\n      \"networks\": [\n        \"MANAGEMENT\",\n        \"VSAN\",\n        \"VMOTION\"\n      ],\n      \"nsxtSwitchConfig\": {\n        \"transportZones\": [\n          {\n            \"name\": \"sfo-m01-tz-overlay01\",\n            \"transportType\": \"OVERLAY\"\n          },\n          {\n            \"name\": \"sfo-m01-tz-vlan01\",\n            \"transportType\": \"VLAN\"\n          }\n        ]\n      }\n    }\n  ],\n  \"clusterSpec\": {\n    \"clusterName\": \"sfo-m01-cl01\",\n    \"clusterEvcMode\": \"\",\n    \"resourcePoolSpecs\": [\n      {\n        \"cpuSharesLevel\": \"high\",\n        \"cpuSharesValue\": 0,\n        \"name\": \"sfo-m01-cl01-rp-sddc-mgmt\",\n        \"memorySharesValue\": 0,\n        \"cpuReservationPercentage\": 0,\n        \"memoryLimit\": -1,\n        \"memoryReservationPercentage\": 0,\n        \"cpuReservationExpandable\": true,\n        \"memoryReservationExpandable\": true,\n        \"memorySharesLevel\": \"normal\",\n        \"cpuLimit\": -1,\n        \"type\": \"management\"\n      },\n      {\n        \"cpuSharesLevel\": \"high\",\n        \"cpuSharesValue\": 0,\n        \"name\": \"sfo-m01-cl01-rp-sddc-network\",\n        \"memorySharesValue\": 0,\n        \"cpuReservationPercentage\": 0,\n        \"memoryLimit\": -1,\n        \"memoryReservationPercentage\": 0,\n        \"cpuReservationExpandable\": true,\n        \"memoryReservationExpandable\": true,\n        \"memorySharesLevel\": \"normal\",\n        \"cpuLimit\": -1,\n        \"type\": \"network\"\n      },\n      {\n        \"cpuSharesLevel\": \"normal\",\n        \"cpuSharesValue\": 0,\n        \"name\": \"sfo-m01-cl01-rp-sddc-compute\",\n        \"memorySharesValue\": 0,\n        \"cpuReservationPercentage\": 0,\n        \"memoryLimit\": -1,\n        \"memoryReservationPercentage\": 0,\n        \"cpuReservationExpandable\": true,\n        \"memoryReservationExpandable\": true,\n        \"memorySharesLevel\": \"normal\",\n        \"cpuLimit\": -1,\n        \"type\": \"compute\"\n      },\n      {\n        \"name\": \"sfo-m01-cl01-rp-user-compute\",\n        \"type\": \"compute\",\n        \"cpuReservationMhz\": 2100,\n        \"cpuLimit\": -1,\n        \"cpuReservationExpandable\": true,\n        \"cpuSharesLevel\": \"normal\",\n        \"memoryReservationMb\": 3128,\n        \"memoryReservationExpandable\": true,\n        \"memorySharesLevel\": \"normal\",\n        \"memorySharesValue\": 0\n      }\n    ]\n  },\n  \"pscSpecs\": [\n    {\n      \"pscSsoSpec\": {\n        \"ssoDomain\": \"vsphere.local\"\n      },\n      \"adminUserSsoPassword\": \"xxxxxxx\"\n    }\n  ],\n  \"vcenterSpec\": {\n    \"vcenterIp\": \"10.0.0.6\",\n    \"vcenterHostname\": \"sfo-m01-vc01\",\n    \"licenseFile\": \"XXXXX-XXXXX-XXXXX-XXXXX-XXXXX\",\n    \"rootVcenterPassword\": \"xxxxxxx\",\n    \"vmSize\": \"tiny\"\n  },\n  \"hostSpecs\": [\n    {\n      \"credentials\": {\n        \"username\": \"root\",\n        \"password\": \"xxxxxxx\"\n      },\n      \"ipAddressPrivate\": {\n        \"subnet\": \"255.255.252.0\",\n        \"cidr\": \"\",\n        \"ipAddress\": \"10.0.0.100\",\n        \"gateway\": \"10.0.0.250\"\n      },\n      \"hostname\": \"sfo01-m01-esx01\",\n      \"association\": \"sfo-m01-dc01\"\n    },\n    {\n      \"credentials\": {\n        \"username\": \"root\",\n        \"password\": \"xxxxxxx\"\n      },\n      \"ipAddressPrivate\": {\n        \"subnet\": \"255.255.252.0\",\n        \"cidr\": \"\",\n        \"ipAddress\": \"10.0.0.101\",\n        \"gateway\": \"10.0.0.250\"\n      },\n      \"hostname\": \"sfo01-m01-esx02\",\n      \"association\": \"sfo-m01-dc01\"\n    },\n    {\n      \"credentials\": {\n        \"username\": \"root\",\n        \"password\": \"xxxxxxx\"\n      },\n      \"ipAddressPrivate\": {\n        \"subnet\": \"255.255.255.0\",\n        \"cidr\": \"\",\n        \"ipAddress\": \"10.0.0.102\",\n        \"gateway\": \"10.0.0.250\"\n      },\n      \"hostname\": \"sfo01-m01-esx03\",\n      \"association\": \"sfo-m01-dc01\"\n    },\n    {\n      \"credentials\": {\n        \"username\": \"root\",\n        \"password\": \"xxxxxxx\"\n      },\n      \"ipAddressPrivate\": {\n        \"subnet\": \"255.255.255.0\",\n        \"cidr\": \"\",\n        \"ipAddress\": \"10.0.0.103\",\n        \"gateway\": \"10.0.0.250\"\n      },\n      \"hostname\": \"sfo01-m01-esx04\",\n      \"association\": \"sfo-m01-dc01\"\n    }\n  ]\n}\n"
            }
            }
            }
            with self.assertRaises(AnsibleExitJson) as result:
                cloud_builder_create_managment_domain.main()
            self.assertFalse(result.exception.args[0]['changed'])

            mock_create_sddc.assert_called_once_with({
            "status_code": 201,
            "message": "Created",
            "data": {
                "id": "26c27804-f837-4e4f-b50f-1625af792f0f",
                "executionStatus": "COMPLETED",
                "validationChecks": [],
                "additionalProperties": {
                "sddcSpec": "{\n  \"dvSwitchVersion\": \"7.0.0\",\n  \"skipEsxThumbprintValidation\": true,\n  \"managementPoolName\": \"bringup-networkpool\",\n  \"sddcManagerSpec\": {\n    \"hostname\": \"sfo-vcf01\",\n    \"ipAddress\": \"10.0.0.4\",\n    \"localUserPassword\": \"xxxxxxxxxxxx\",\n    \"rootUserCredentials\": {\n      \"username\": \"root\",\n      \"password\": \"xxxxxxx\"\n    },\n    \"secondUserCredentials\": {\n      \"username\": \"vcf\",\n      \"password\": \"xxxxxxx\"\n    }\n  },\n  \"sddcId\": \"sddcId-public-api-01\",\n  \"esxLicense\": \"XXXXX-XXXXX-XXXXX-XXXXX-XXXXX\",\n  \"workflowType\": \"VCF\",\n  \"ntpServers\": [\n    \"10.0.0.250\"\n  ],\n  \"dnsSpec\": {\n    \"subdomain\": \"vrack.vsphere.local\",\n    \"domain\": \"vsphere.local\",\n    \"nameserver\": \"10.0.0.250\",\n    \"secondaryNameserver\": \"10.0.0.251\"\n  },\n  \"networkSpecs\": [\n    {\n      \"subnet\": \"10.0.0.0/22\",\n      \"vlanId\": \"0\",\n      \"mtu\": \"1500\",\n      \"networkType\": \"MANAGEMENT\",\n      \"gateway\": \"10.0.0.250\"\n    },\n    {\n      \"subnet\": \"10.0.4.0/24\",\n      \"includeIpAddressRanges\": [\n        {\n          \"startIpAddress\": \"10.0.4.7\",\n          \"endIpAddress\": \"10.0.4.48\"\n        },\n        {\n          \"startIpAddress\": \"10.0.4.3\",\n          \"endIpAddress\": \"10.0.4.6\"\n        }\n      ],\n      \"includeIpAddress\": [\n        \"10.0.4.50\",\n        \"10.0.4.49\"\n      ],\n      \"vlanId\": \"0\",\n      \"mtu\": \"8940\",\n      \"networkType\": \"VSAN\",\n      \"gateway\": \"10.0.4.253\"\n    },\n    {\n      \"subnet\": \"10.0.8.0/24\",\n      \"includeIpAddressRanges\": [\n        {\n          \"startIpAddress\": \"10.0.8.3\",\n          \"endIpAddress\": \"10.0.8.50\"\n        }\n      ],\n      \"vlanId\": \"0\",\n      \"mtu\": \"8940\",\n      \"networkType\": \"VMOTION\",\n      \"gateway\": \"10.0.8.253\"\n    }\n  ],\n  \"nsxtSpec\": {\n    \"nsxtManagerSize\": \"medium\",\n    \"nsxtManagers\": [\n      {\n        \"hostname\": \"sfo-m01-nsx01a\",\n        \"ip\": \"10.0.0.31\"\n      },\n      {\n        \"hostname\": \"sfo-m01-nsx01b\",\n        \"ip\": \"10.0.0.32\"\n      },\n      {\n        \"hostname\": \"sfo-m01-nsx01c\",\n        \"ip\": \"10.0.0.33\"\n      }\n    ],\n    \"rootNsxtManagerPassword\": \"xxxxxxx\",\n    \"nsxtAdminPassword\": \"xxxxxxx\",\n    \"nsxtAuditPassword\": \"xxxxxxx\",\n    \"vip\": \"10.0.0.30\",\n    \"vipFqdn\": \"sfo-m01-nsx01\",\n    \"nsxtLicense\": \"XXXXX-XXXXX-XXXXX-XXXXX-XXXXX\",\n    \"transportVlanId\": 0,\n    \"ipAddressPoolSpec\": {\n      \"name\": \"sfo01-m01-cl01-tep01\",\n      \"description\": \"ESXi Host Overlay TEP IP Pool\",\n      \"subnets\": [\n        {\n          \"ipAddressPoolRanges\": [\n            {\n              \"start\": \"172.16.14.101\",\n              \"end\": \"172.16.14.108\"\n            }\n          ],\n          \"cidr\": \"172.16.14.0/24\",\n          \"gateway\": \"172.16.14.1\"\n        }\n      ]\n    }\n  },\n  \"vsanSpec\": {\n    \"licenseFile\": \"XXXXX-XXXXX-XXXXX-XXXXX-XXXXX\",\n    \"datastoreName\": \"sfo-m01-cl01-ds-vsan01\",\n    \"esaConfig\": {\n      \"enabled\": false\n    }\n  },\n  \"dvsSpecs\": [\n    {\n      \"mtu\": 8940,\n      \"niocSpecs\": [\n        {\n          \"trafficType\": \"VSAN\",\n          \"value\": \"HIGH\"\n        },\n        {\n          \"trafficType\": \"VMOTION\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"VDP\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"VIRTUALMACHINE\",\n          \"value\": \"HIGH\"\n        },\n        {\n          \"trafficType\": \"MANAGEMENT\",\n          \"value\": \"NORMAL\"\n        },\n        {\n          \"trafficType\": \"NFS\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"HBR\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"FAULTTOLERANCE\",\n          \"value\": \"LOW\"\n        },\n        {\n          \"trafficType\": \"ISCSI\",\n          \"value\": \"LOW\"\n        }\n      ],\n      \"dvsName\": \"sfo-m01-cl01-vds01\",\n      \"vmnicsToUplinks\": [\n        {\n          \"id\": \"vmnic0\",\n          \"uplink\": \"uplink1\"\n        },\n        {\n          \"id\": \"vmnic1\",\n          \"uplink\": \"uplink2\"\n        }\n      ],\n      \"nsxTeamings\": [\n        {\n          \"policy\": \"LOADBALANCE_SRCID\",\n          \"activeUplinks\": [\n            \"uplink1\",\n            \"uplink2\"\n          ],\n          \"standByUplinks\": []\n        }\n      ],\n      \"networks\": [\n        \"MANAGEMENT\",\n        \"VSAN\",\n        \"VMOTION\"\n      ],\n      \"nsxtSwitchConfig\": {\n        \"transportZones\": [\n          {\n            \"name\": \"sfo-m01-tz-overlay01\",\n            \"transportType\": \"OVERLAY\"\n          },\n          {\n            \"name\": \"sfo-m01-tz-vlan01\",\n            \"transportType\": \"VLAN\"\n          }\n        ]\n      }\n    }\n  ],\n  \"clusterSpec\": {\n    \"clusterName\": \"sfo-m01-cl01\",\n    \"clusterEvcMode\": \"\",\n    \"resourcePoolSpecs\": [\n      {\n        \"cpuSharesLevel\": \"high\",\n        \"cpuSharesValue\": 0,\n        \"name\": \"sfo-m01-cl01-rp-sddc-mgmt\",\n        \"memorySharesValue\": 0,\n        \"cpuReservationPercentage\": 0,\n        \"memoryLimit\": -1,\n        \"memoryReservationPercentage\": 0,\n        \"cpuReservationExpandable\": true,\n        \"memoryReservationExpandable\": true,\n        \"memorySharesLevel\": \"normal\",\n        \"cpuLimit\": -1,\n        \"type\": \"management\"\n      },\n      {\n        \"cpuSharesLevel\": \"high\",\n        \"cpuSharesValue\": 0,\n        \"name\": \"sfo-m01-cl01-rp-sddc-network\",\n        \"memorySharesValue\": 0,\n        \"cpuReservationPercentage\": 0,\n        \"memoryLimit\": -1,\n        \"memoryReservationPercentage\": 0,\n        \"cpuReservationExpandable\": true,\n        \"memoryReservationExpandable\": true,\n        \"memorySharesLevel\": \"normal\",\n        \"cpuLimit\": -1,\n        \"type\": \"network\"\n      },\n      {\n        \"cpuSharesLevel\": \"normal\",\n        \"cpuSharesValue\": 0,\n        \"name\": \"sfo-m01-cl01-rp-sddc-compute\",\n        \"memorySharesValue\": 0,\n        \"cpuReservationPercentage\": 0,\n        \"memoryLimit\": -1,\n        \"memoryReservationPercentage\": 0,\n        \"cpuReservationExpandable\": true,\n        \"memoryReservationExpandable\": true,\n        \"memorySharesLevel\": \"normal\",\n        \"cpuLimit\": -1,\n        \"type\": \"compute\"\n      },\n      {\n        \"name\": \"sfo-m01-cl01-rp-user-compute\",\n        \"type\": \"compute\",\n        \"cpuReservationMhz\": 2100,\n        \"cpuLimit\": -1,\n        \"cpuReservationExpandable\": true,\n        \"cpuSharesLevel\": \"normal\",\n        \"memoryReservationMb\": 3128,\n        \"memoryReservationExpandable\": true,\n        \"memorySharesLevel\": \"normal\",\n        \"memorySharesValue\": 0\n      }\n    ]\n  },\n  \"pscSpecs\": [\n    {\n      \"pscSsoSpec\": {\n        \"ssoDomain\": \"vsphere.local\"\n      },\n      \"adminUserSsoPassword\": \"xxxxxxx\"\n    }\n  ],\n  \"vcenterSpec\": {\n    \"vcenterIp\": \"10.0.0.6\",\n    \"vcenterHostname\": \"sfo-m01-vc01\",\n    \"licenseFile\": \"XXXXX-XXXXX-XXXXX-XXXXX-XXXXX\",\n    \"rootVcenterPassword\": \"xxxxxxx\",\n    \"vmSize\": \"tiny\"\n  },\n  \"hostSpecs\": [\n    {\n      \"credentials\": {\n        \"username\": \"root\",\n        \"password\": \"xxxxxxx\"\n      },\n      \"ipAddressPrivate\": {\n        \"subnet\": \"255.255.252.0\",\n        \"cidr\": \"\",\n        \"ipAddress\": \"10.0.0.100\",\n        \"gateway\": \"10.0.0.250\"\n      },\n      \"hostname\": \"sfo01-m01-esx01\",\n      \"association\": \"sfo-m01-dc01\"\n    },\n    {\n      \"credentials\": {\n        \"username\": \"root\",\n        \"password\": \"xxxxxxx\"\n      },\n      \"ipAddressPrivate\": {\n        \"subnet\": \"255.255.252.0\",\n        \"cidr\": \"\",\n        \"ipAddress\": \"10.0.0.101\",\n        \"gateway\": \"10.0.0.250\"\n      },\n      \"hostname\": \"sfo01-m01-esx02\",\n      \"association\": \"sfo-m01-dc01\"\n    },\n    {\n      \"credentials\": {\n        \"username\": \"root\",\n        \"password\": \"xxxxxxx\"\n      },\n      \"ipAddressPrivate\": {\n        \"subnet\": \"255.255.255.0\",\n        \"cidr\": \"\",\n        \"ipAddress\": \"10.0.0.102\",\n        \"gateway\": \"10.0.0.250\"\n      },\n      \"hostname\": \"sfo01-m01-esx03\",\n      \"association\": \"sfo-m01-dc01\"\n    },\n    {\n      \"credentials\": {\n        \"username\": \"root\",\n        \"password\": \"xxxxxxx\"\n      },\n      \"ipAddressPrivate\": {\n        \"subnet\": \"255.255.255.0\",\n        \"cidr\": \"\",\n        \"ipAddress\": \"10.0.0.103\",\n        \"gateway\": \"10.0.0.250\"\n      },\n      \"hostname\": \"sfo01-m01-esx04\",\n      \"association\": \"sfo-m01-dc01\"\n    }\n  ]\n}\n"
            }
            }
            })