from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest

from unittest.mock import MagicMock
from ansible_collections.vmware.vcf.plugins.moduleutils.cloud_builder import CloudBuilderApiClient
from ansible_collections.vmware.vcf.plugins.moduleutils.exceptions import VcfAPIException


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

FETCH_URL_JSON_SUCCESS = [
    (
        (None, dict(
            body=json.dumps(dict(
                a='b'
            )).encode('utf-8'),
        )),
        None,
        (dict(
            a='b'
        ), None)
    ),
    (
        (None, dict(
            body=json.dumps(dict(
                error=dict(
                    code="foo",
                    status=400,
                    message="bar",
                ),
                a='b'
            )).encode('utf-8'),
        )),
        ['foo'],
        (dict(
            error=dict(
                code="foo",
                status=400,
                message="bar",
            ),
            a='b'
        ), 'foo')
    ),
]


FETCH_URL_JSON_FAIL = [
    (
        (None, dict(
            body=json.dumps(dict(
                error=dict(
                    code="foo",
                    status=400,
                    message="bar",
                ),
            )).encode('utf-8'),
        )),
        None,
        'Request failed: 400 foo (bar)',
        {
            'error': {
                'code': "foo",
                'status': 400,
                'message': "bar",
            },
        },
    ),
    (
        (None, dict(
            body=json.dumps(dict(
                error=dict(
                    code="foo",
                    status=400,
                    message="bar",
                    missing=None,
                    invalid=None,
                    max_request=None,
                    interval=None,
                ),
            )).encode('utf-8'),
        )),
        ['bar'],
        'Request failed: 400 foo (bar)',
        {
            'error': {
                'code': "foo",
                'status': 400,
                'message': "bar",
                'missing': None,
                'invalid': None,
                'max_request': None,
                'interval': None,
            },
        },
    ),
    (
        (None, dict(
            body=json.dumps(dict(
                error=dict(
                    code="foo",
                    status=400,
                    message="bar",
                    missing=["foo"],
                    invalid=["bar"],
                    max_request=0,
                    interval=0,
                ),
            )).encode('utf-8'),
        )),
        None,
        "Request failed: 400 foo (bar). Missing input parameters: ['foo']. Invalid input"
        " parameters: ['bar']. Maximum allowed requests: 0. Time interval in seconds: 0",
        {
            'error': {
                'code': "foo",
                'status': 400,
                'message': "bar",
                'missing': ["foo"],
                'invalid': ["bar"],
                'max_request': 0,
                'interval': 0,
            },
        },
    ),
    (
        (None, dict(body='{this is not json}'.encode('utf-8'))),
        [],
        'Cannot decode content retrieved from https://foo/bar',
        {},
    ),
    (
        (None, dict(status=400)),
        [],
        'Cannot retrieve content from https://foo/bar, HTTP status code 400',
        {},
    ),
]

class TestYourClass(unittest.TestCase):

    # def test_cloud_builder_api_client(self):
    #     module = get_module_mock()
    #     module.params = {
    #         'cloud_builder_ip': '

if __name__ == '__main__':
    unittest.main()