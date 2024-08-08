import sys
import os
import json
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
from ansible_collections.vmware.vcf.plugins.modules import cloud_builder_sddc_validation

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../../../lib/python3.10/site-packages'))


def exit_json(*args, **kwargs):
    raise AnsibleExitJson(kwargs)

def fail_json(*args, **kwargs):
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)

class AnsibleExitJson(Exception):
    pass

class AnsibleFailJson(Exception):
    pass

def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)

class TestCloudBuilderApiClient(TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    @patch('ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder.CloudBuilderApiClient.validate_sddc')
    def test_create_management_domain_validation_success(self, MockCreateSddc):
        MockCreateSddc.return_value = {
            "status_code": 201,
            "message": "Created",
            "data": {
                "id": "26c27804-f837-4e4f-b50f-1625af792f0f",
                "executionStatus": "IN_PROGRESS",
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
                # Truncated for brevity
                # Check https://developer.broadcom.com/xapis/vmware-cloud-foundation-api/latest/sddc/ for full payload
            }
            }
        })
        print(f"mock instance: {MockCreateSddc}")
        with self.assertRaises(AnsibleExitJson) as result:
            cloud_builder_sddc_validation.main()
        
        # Debugging statement to check if create_sddc was called
        print(f"create_sddc called: {MockCreateSddc.called}")
        
        MockCreateSddc.assert_called_once()
        
        # Debugging statement to print the exception args
        print(f"Exception args: {result.exception.args[0]}")
        
        # Check the actual keys in the exception args
        self.assertIn('status_code', result.exception.args[0])
        self.assertEqual(result.exception.args[0]['status_code'], 201)
        
        # Accessing data from the result dictionary
        payload_data = result.exception.args[0]['meta']
        print(f"Payload Data: {payload_data}")

    @patch('ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder.CloudBuilderApiClient.validate_sddc')
    def test_validate_sddc_failure_400(self, MockValidateSddc):
        MockValidateSddc.side_effect = VcfAPIException("Invalid input", status_code=400)
        set_module_args({
            'cloud_builder_ip': 'sfo-cb01.rainpole.local',
            'cloud_builder_user': 'admin',
            'cloud_builder_password': 'VMware1!',
            'sddc_management_domain_payload': {
                "dvSwitchVersion": "7.0.0",
                "skipEsxThumbprintValidation": True,
                "managementPoolName": "bringup-networkpool",
                "sddcManagerSpec": {
                    # Truncated for brevity
                }
            }
        })

        with self.assertRaises(AnsibleFailJson) as result:
            cloud_builder_sddc_validation.main()
        
        MockValidateSddc.assert_called_once()
        
        self.assertIn('status_code', result.exception.args[0])
        self.assertEqual(result.exception.args[0]['status_code'], 400)
        
        # Check that the exception contains the expected status code and message
        self.assertIn('status_code', result.exception.args[0])
        self.assertEqual(result.exception.args[0]['status_code'], 400)
        self.assertIn('msg', result.exception.args[0])
        self.assertIn("Invalid input", result.exception.args[0]['msg'])

    @patch('ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder.CloudBuilderApiClient.validate_sddc')
    def test_validate_sddc_failure_500(self, MockValidateSddc):
        # Mock the return value of validate_sddc to simulate a server error
        MockValidateSddc.side_effect = VcfAPIException("Internal Server Error", status_code=500)

        # Set the arguments for the module
        set_module_args({
            'cloud_builder_ip': 'sfo-cb01.rainpole.local',
            'cloud_builder_user': 'admin',
            'cloud_builder_password': 'VMware1!',
            'sddc_management_domain_payload': {
                "dvSwitchVersion": "7.0.0",
                "skipEsxThumbprintValidation": True,
                "managementPoolName": "bringup-networkpool",
                "sddcManagerSpec": {
                    # Truncated for brevity
                }
            }
        })

        # Call the main function and expect an AnsibleFailJson exception
        with self.assertRaises(AnsibleFailJson) as result:
            cloud_builder_sddc_validation.main()

        # Verify that validate_sddc was called exactly once
        MockValidateSddc.assert_called_once()

        # Check that the exception contains the expected status code and message
        self.assertIn('status_code', result.exception.args[0])
        self.assertEqual(result.exception.args[0]['status_code'], 500)
        self.assertIn('msg', result.exception.args[0])
        self.assertIn('Internal Server Error', result.exception.args[0]['msg'])

    #############################################################
    # Test Cloud Builder API Client Create SDDC Management Domain
    #############################################################
    @patch('ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder.CloudBuilderApiClient.create_sddc')
    def test_create_management_domain_success(self, MockCreateSddc):
        MockCreateSddc.return_value = {
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
                    # Truncated for brevity
                }
            }
        })

        print(f"mock instance: {MockCreateSddc}")
        with self.assertRaises(AnsibleExitJson) as result:
            cloud_builder_create_management_domain.main()
        
        print(f"create_sddc called: {MockCreateSddc.called}")
        
        MockCreateSddc.assert_called_once()
        
        print(f"Exception args: {result.exception.args[0]}")
        
        self.assertIn('status_code', result.exception.args[0])
        self.assertEqual(result.exception.args[0]['status_code'], 201)
        
        payload_data = result.exception.args[0]['meta']
        self.assertIsNotNone(payload_data)

    @patch('ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder.CloudBuilderApiClient.create_sddc')
    def test_create_management_domain_failure_400(self, MockCreateSddc):
        MockCreateSddc.side_effect = VcfAPIException("Invalid input", status_code=400)
        set_module_args({
            'cloud_builder_ip': 'sfo-cb01.rainpole.local',
            'cloud_builder_user': 'admin',
            'cloud_builder_password': 'VMware1!',
            'sddc_management_domain_payload': {
                "dvSwitchVersion": "7.0.0",
                "skipEsxThumbprintValidation": True,
                "managementPoolName": "bringup-networkpool",
                "sddcManagerSpec": {
                    # Truncated for brevity
                }
            }
        })

        with self.assertRaises(AnsibleFailJson) as result:
            cloud_builder_create_management_domain.main()
        
        MockCreateSddc.assert_called_once()
        
        self.assertIn('status_code', result.exception.args[0])
        self.assertEqual(result.exception.args[0]['status_code'], 400)
        
        # Check that the exception contains the expected status code and message
        self.assertIn('status_code', result.exception.args[0])
        self.assertEqual(result.exception.args[0]['status_code'], 400)
        self.assertIn('msg', result.exception.args[0])
        self.assertIn("Invalid input", result.exception.args[0]['msg'])

    @patch('ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder.CloudBuilderApiClient.create_sddc')
    def test_create_management_domain_failure_500(self, MockCreateSddc):
        # Mock the return value of create_sddc to simulate a server error
    # Mock the create_sddc method to raise a VcfAPIException
        MockCreateSddc.side_effect = VcfAPIException("Internal Server Error", status_code=500)


        # Set the arguments for the module
        set_module_args({
            'cloud_builder_ip': 'sfo-cb01.rainpole.local',
            'cloud_builder_user': 'admin',
            'cloud_builder_password': 'VMware1!',
            'sddc_management_domain_payload': {
                "dvSwitchVersion": "7.0.0",
                "skipEsxThumbprintValidation": True,
                "managementPoolName": "bringup-networkpool",
                "sddcManagerSpec": {
                    # Truncated for brevity
                }
            }
        })

        # Call the main function and expect an AnsibleFailJson exception
        with self.assertRaises(AnsibleFailJson) as result:
            cloud_builder_create_management_domain.main()

        # Verify that create_sddc was called exactly once
        MockCreateSddc.assert_called_once()

        # Check that the exception contains the expected status code and message
        self.assertIn('status_code', result.exception.args[0])
        self.assertEqual(result.exception.args[0]['status_code'], 500)
        self.assertIn('msg', result.exception.args[0])
        self.assertIn('Internal Server Error', result.exception.args[0]['msg'])

if __name__ == '__main__':
    unittest.main()
