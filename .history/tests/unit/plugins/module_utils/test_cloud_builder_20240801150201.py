from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest

from unittest.mock import MagicMock
from ansible.module_utils import cloud_builder
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


@pytest.mark.parametrize("return_value, accept_errors, result", FETCH_URL_JSON_SUCCESS)
def test_fetch_url_json(monkeypatch, return_value, accept_errors, result):
    module = get_module_mock()
    cloud_builder.fetch_url = MagicMock(return_value=return_value)

    assert cloud_builder.fetch_url_json(module, 'https://foo/bar', accept_errors=accept_errors) == result


@pytest.mark.parametrize("return_value, accept_errors, fail_msg, fail_kwargs", FETCH_URL_JSON_FAIL)
def test_fetch_url_json_fail(monkeypatch, return_value, accept_errors, fail_msg, fail_kwargs):
    module = get_module_mock()
    cloud_builder.fetch_url = MagicMock(return_value=return_value)

    with pytest.raises(ModuleFailException) as exc:
        cloud_builder.fetch_url_json(module, 'https://foo/bar', accept_errors=accept_errors)

    print(exc.value.fail_msg)
    print(exc.value.fail_kwargs)
    assert exc.value.fail_msg == fail_msg
    assert exc.value.fail_kwargs == fail_kwargs


def test_fetch_url_json_empty(monkeypatch):
    module = get_module_mock()
    cloud_builder.fetch_url = MagicMock(return_value=(None, dict(status=204, body='')))

    assert cloud_builder.fetch_url_json(module, 'https://foo/bar', allow_empty_result=True) == (None, None)

    cloud_builder.fetch_url = MagicMock(return_value=(None, dict(status=400, body='')))

    with pytest.raises(ModuleFailException) as exc:
        cloud_builder.fetch_url_json(module, 'https://foo/bar', allow_empty_result=True)

    print(exc.value.fail_msg)
    print(exc.value.fail_kwargs)
    assert exc.value.fail_msg == 'Cannot retrieve content from https://foo/bar, HTTP status code 400'
    assert exc.value.fail_kwargs == dict()


@pytest.mark.parametrize("return_value, accept_errors, result", FETCH_URL_JSON_SUCCESS)
def test_plugin_open_url_json(monkeypatch, return_value, accept_errors, result):
    response = MagicMock()
    response.read = MagicMock(return_value=return_value[1]['body'])
    cloud_builder.open_url = MagicMock(return_value=response)
    plugin = MagicMock()

    assert cloud_builder.plugin_open_url_json(plugin, 'https://foo/bar', accept_errors=accept_errors) == result


@pytest.mark.parametrize("return_value, accept_errors, fail_msg, fail_kwargs", FETCH_URL_JSON_FAIL)
def test_plugin_open_url_json_fail(monkeypatch, return_value, accept_errors, fail_msg, fail_kwargs):
    response = MagicMock()
    response.read = MagicMock(return_value=return_value[1].get('body', ''))
    cloud_builder.open_url = MagicMock(side_effect=cloud_builder.HTTPError('https://foo/bar', 400, 'Error!', {}, response))
    plugin = MagicMock()

    with pytest.raises(cloud_builder.PluginException) as exc:
        cloud_builder.plugin_open_url_json(plugin, 'https://foo/bar', accept_errors=accept_errors)

    print(exc.value.error_message)
    assert exc.value.error_message == fail_msg


def test_plugin_open_url_json_fail_other(monkeypatch):
    cloud_builder.open_url = MagicMock(side_effect=Exception('buh!'))
    plugin = MagicMock()

    with pytest.raises(cloud_builder.PluginException) as exc:
        cloud_builder.plugin_open_url_json(plugin, 'https://foo/bar')

    assert exc.value.error_message == 'Failed request to Hetzner cloud_builder server endpoint https://foo/bar: buh!'


def test_plugin_open_url_json_fail_other_2(monkeypatch):
    response = MagicMock()
    response.read = MagicMock(side_effect=AttributeError('read'))
    cloud_builder.open_url = MagicMock(side_effect=cloud_builder.HTTPError('https://foo/bar', 400, 'Error!', {}, response))
    plugin = MagicMock()

    with pytest.raises(cloud_builder.PluginException) as exc:
        cloud_builder.plugin_open_url_json(plugin, 'https://foo/bar')

    assert exc.value.error_message == 'Cannot retrieve content from https://foo/bar, HTTP status code 400'


def test_plugin_open_url_json_empty_result(monkeypatch):
    response = MagicMock()
    response.read = MagicMock(return_value='')
    response.code = 200
    cloud_builder.open_url = MagicMock(return_value=response)
    plugin = MagicMock()

    assert cloud_builder.plugin_open_url_json(plugin, 'https://foo/bar', allow_empty_result=True) == (None, None)

    response = MagicMock()
    response.read = MagicMock(side_effect=AttributeError('read'))
    cloud_builder.open_url = MagicMock(side_effect=cloud_builder.HTTPError('https://foo/bar', 400, 'Error!', {}, response))

    with pytest.raises(cloud_builder.PluginException) as exc:
        cloud_builder.plugin_open_url_json(plugin, 'https://foo/bar')

    assert exc.value.error_message == 'Cannot retrieve content from https://foo/bar, HTTP status code 400'