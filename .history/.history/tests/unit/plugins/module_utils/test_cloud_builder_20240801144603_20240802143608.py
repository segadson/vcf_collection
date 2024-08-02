from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest

from unittest.mock import MagicMock
from ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder import CloudBuilderApiClient
from ansible_collections.vmware.vcf.plugins.module_utils.exceptions import VcfAPIException


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

class TestYourClass(unittest.TestCase):

    @patch('your_module.YourDependency')
    def setUp(self, MockDependency):
        self.mock_dependency = MockDependency.return_value
        self.module = MagicMock()
        self.your_class_instance = YourClass(
            param1='value1',
            param2='value2',
            module=self.module
        )

    @patch.object(YourClass, 'your_method', return_value={
        "key": "value"
    })
    def test_your_method(self, mock_method):
        self.your_class_instance.state = 'some_state'
        
        # Define the payload
        payload = {
            "key": "value"
        }
        
        # Pass the payload to the method
        self.your_class_instance.run(payload)
        
        # Verify that your_method was called with the payload
        mock_method.assert_called_once_with(payload)
        
        # Verify that exit_json was called with the expected arguments
        self.module.exit_json.assert_called_once_with(changed=True, meta={
            "key": "value"
        })

    def test_invalid_state(self):
        self.your_class_instance.state = 'invalid_state'
        
        # Run the method
        self.your_class_instance.run({})
        
        # Verify that fail_json was called with the expected arguments
        self.module.fail_json.assert_called_once_with(msg="Error: Invalid State")

if __name__ == '__main__':
    unittest.main()