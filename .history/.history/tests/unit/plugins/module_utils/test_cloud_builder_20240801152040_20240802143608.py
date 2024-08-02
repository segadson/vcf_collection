from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest

from unittest.mock import MagicMock
from ansible_collections.vmware.vcf.plugins.module__utils import cloud_builder


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
