import json
import unittest
from unittest.mock import patch, MagicMock
from ansible_collections.vmware.vcf.plugins.module_utils import basic
from ansible_collections.vmware.vcf.plugins.module_utils.common.text.converters import to_bytes
from sddc_manager_network_pools import SddcManagerNetworkPools
from community.internal_test_tools import AnsibleExitJson, AnsibleFailJson

class SddcManagerNetworkPools:
    # Assuming other methods and initializations are here

    def run(self):
        if self.state == 'create':
            result = self.network_pools_create()
            self.module.exit_json(**AnsibleExitJson(changed=True, meta=result).to_dict())
        elif self.state == 'update':
            result = self.network_pools_update()
            self.module.exit_json(**AnsibleExitJson(changed=True, meta=result).to_dict())
        elif self.state == 'delete':
            result = self.network_pools_delete()
            self.module.exit_json(**AnsibleExitJson(changed=False, meta=result).to_dict())
        else:
            self.module.fail_json(**AnsibleFailJson(msg="Error: Invalid State").to_dict())

class TestSddcManagerNetworkPools(unittest.TestCase):

    @patch('sddc_manager_network_pools.SddcManagerApiClient')
    def setUp(self, MockApiClient):
        self.mock_api_client = MockApiClient.return_value
        self.module = MagicMock()
        self.sddc_manager = SddcManagerNetworkPools(
            sddc_manager_ip='192.168.1.1',
            sc_manager_user='admin',
            sddc_manager_password='password',
            module=self.module
        )

    @patch.object(SddcManagerNetworkPools, 'network_pools_create', return_value={
        "id": "8f88f54d-c25a-4c9e-9c1d-b155445cc1ca",
        "name": "engineering-networkpool",
        "networks": [{
            "id": "ec64b676-1184-4c11-8f1b-6966ffdb9a39"
        }]
    })
    def test_run_create(self, mock_create):
        self.sddc_manager.state = 'create'
        
        # Define the payload
        payload = {
            "name": "engineering-networkpool",
            "networks": [
                {
                    "type": "VSAN",
                    "vlanId": 3002,
                    "mtu": 9001,
                    "subnet": "192.168.8.0",
                    "mask": "255.255.252.0",
                    "gateway": "192.168.8.1",
                    "ipPools": [
                        {
                            "start": "192.168.8.5",
                            "end": "192.168.8.8"
                        }
                    ]
                }
            ]
        }
        
        # Pass the payload to the run method
        self.sddc_manager.run(payload)
        
        # Verify that network_pools_create was called with the payload
        mock_create.assert_called_once_with(payload)
        
        # Verify that exit_json was called with the expected arguments
        self.module.exit_json.assert_called_once_with(changed=True, meta={
            "id": "8f88f54d-c25a-4c9e-9c1d-b155445cc1ca",
            "name": "engineering-networkpool",
            "networks": [{
                "id": "ec64b676-1184-4c11-8f1b-6966ffdb9a39"
            }]
        })

if __name__ == '__main__':
    unittest.main()