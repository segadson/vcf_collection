import pytest
from ansible.module_utils.basic import AnsibleModule
from units.modules.utils import set_module_args
from ansible.module_utils.common.text.converters import to_bytes

class AnsibleExitJson(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs

class AnsibleFailJson(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs

def exit_json(*args, **kwargs):
    raise AnsibleExitJson(kwargs)

def fail_json(*args, **kwargs):
    raise AnsibleFailJson(kwargs)

@pytest.fixture
def patch_ansible_module(mocker):
    mocker.patch('ansible.module_utils.basic.AnsibleModule.exit_json', side_effect=exit_json)
    mocker.patch('ansible.module_utils.basic.AnsibleModule.fail_json', side_effect=fail_json)
