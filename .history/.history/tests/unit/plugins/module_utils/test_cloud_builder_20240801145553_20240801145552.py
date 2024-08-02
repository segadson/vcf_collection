from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest

from unittest.mock import MagicMock
from ansible.module_utils.cloud_builder import CloudBuilderApiClient
from ansible.module_utils.exceptions import VcfAPIException


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

    # def test_cloud_builder_api_client(self):
    #     module = get_module_mock()
    #     module.params = {
    #         'cloud_builder_ip': '

if __name__ == '__main__':
    unittest.main()