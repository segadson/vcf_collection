import unittest
from unittest.mock import patch, MagicMock
from sddc_manager_network_pools import SddcManagerNetworkPools, VcfAPIException

class AnsibleExitJson:
    def __init__(self, changed, meta):
        self.changed = changed
        self.meta = meta

    def to_dict(self):
        return {
            'changed': self.changed,
            'meta': self.meta
        }

class AnsibleFailJson:
    def __init__(self, msg):
        self.msg = msg

    def to_dict(self):
        return {
            'msg': self.msg
        }
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

    @patch.object(SddcManagerNetworkPools, 'network_pools_create', return_value={'id': '123'})
    def test_run_create(self, mock_create):
        self.sddc_manager.state = 'create'
        self.sddc_manager.run()
        mock_create.assert_called_once()
        self.module.exit_json.assert_called_once_with(changed=True, meta={'id': '123'})

    @patch.object(SddcManagerNetworkPools, 'network_pools_update', return_value={'id': '123'})
    def test_run_update(self, mock_update):
        self.sddc_manager.state = 'update'
        self.sddc_manager.run()
        mock_update.assert_called_once()
        self.module.exit_json.assert_called_once_with(changed=True, meta={'id': '123'})

    @patch.object(SddcManagerNetworkPools, 'network_pools_delete', return_value={'id': '123'})
    def test_run_delete(self, mock_delete):
        self.sddc_manager.state = 'delete'
        self.sddc_manager.run()
        mock_delete.assert_called_once()
        self.module.exit_json.assert_called_once_with(changed=False, meta={'id': '123'})

    def test_run_invalid_state(self):
        self.sddc_manager.state = 'invalid'
        self.sddc_manager.run()
        self.module.fail_json.assert_called_once_with(msg="Error: Invalid State")

if __name__ == '__main__':
    unittest.main()