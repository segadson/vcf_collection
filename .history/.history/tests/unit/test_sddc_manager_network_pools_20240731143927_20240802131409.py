import pytest
from unittest.mock import patch, Mock
from ansible_collections.vmware.vcf.plugins.moduleutils.basic import AnsibleModule
from plugins.modules.sddc_manager_network_pools import NetworkPoolManager, VcfAPIException
from mock_sddc_manager import MockSddcManagerApiClient

class MockSddcManagerApiClient:
    def __init__(self):