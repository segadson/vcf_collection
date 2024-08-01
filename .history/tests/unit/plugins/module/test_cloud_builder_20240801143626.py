import unittest
from unittest.mock import patch, MagicMock
from community.internal_test_tools import AnsibleExitJson, AnsibleFailJson
from your_module import YourClass, YourException

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