import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
plugins_dir = os.path.join(current_dir, 'plugins')


import unittest
from unittest.mock import MagicMock
from cloud_builder import CloudBuilderApiClient

class TestCloudBuilderApiClient(unittest.TestCase):

    def setUp(self):
        self.api_client = CloudBuilderApiClient("cloud_builder_ip", "cloud_builder_user", "cloud_builder_password")

    def test_get_sddc(self):
        # Mock the requests library
        self.api_client.sddc_operations = MagicMock(return_value={"status_code": 200, "message": "Success", "data": []})

        # Call the method under test
        result = self.api_client.get_sddc("sddc_id")

        # Assert the expected result
        self.assertEqual(result, {"status_code": 200, "message": "Success", "data": []})
        self.api_client.sddc_operations.assert_called_once_with("GET", "sddc_id")

    def test_create_sddc(self):
        # Mock the requests library
        self.api_client.sddc_operations = MagicMock(return_value={"status_code": 201, "message": "Created", "data": {}})

        # Call the method under test
        result = self.api_client.create_sddc("sddc_id", "sddc_management_domain_payload")

        # Assert the expected result
        self.assertEqual(result, {"status_code": 201, "message": "Created", "data": {}})
        self.api_client.sddc_operations.assert_called_once_with("POST", "sddc_id", "sddc_management_domain_payload")

    def test_retry_sddc(self):
        # Mock the requests library
        self.api_client.sddc_operations = MagicMock(return_value={"status_code": 200, "message": "Success", "data": {}})

        # Call the method under test
        result = self.api_client.retry_sddc("sddc_id", "sddc_management_domain_payload")

        # Assert the expected result
        self.assertEqual(result, {"status_code": 200, "message": "Success", "data": {}})
        self.api_client.sddc_operations.assert_called_once_with("PATCH", "sddc_id", "sddc_management_domain_payload")
    
    def test_get_sddc_failure(self):
        # Mock the requests library to simulate a failure
        self.api_client.sddc_operations = MagicMock(side_effect=Exception("Simulated failure"))

        # Call the method under test and assert that it raises an exception
        with self.assertRaises(Exception) as context:
            self.api_client.get_sddc("sddc_id")

        self.assertTrue("Simulated failure" in str(context.exception))

    def test_create_sddc_failure(self):
        # Mock the requests library to simulate a failure
        self.api_client.sddc_operations = MagicMock(side_effect=Exception("Simulated failure"))

        # Call the method under test and assert that it raises an exception
        with self.assertRaises(Exception) as context:
            self.api_client.create_sddc("sddc_id", "sddc_management_domain_payload")

        self.assertTrue("Simulated failure" in str(context.exception))

    def test_retry_sddc_failure(self):
        # Mock the requests library to simulate a failure
        self.api_client.sddc_operations = MagicMock(side_effect=Exception("Simulated failure"))

        # Call the method under test and assert that it raises an exception
        with self.assertRaises(Exception) as context:
            self.api_client.retry_sddc("sddc_id", "sddc_management_domain_payload")

        self.assertTrue("Simulated failure" in str(context.exception))

    
        '''
        To Do:
        - Add the Rest of the test cases 
        - Add failures 
        - Add Responses
        '''

if __name__ == '__main__':
    unittest.main()