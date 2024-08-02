import pytest
from unittest.mock import Mock, patch
from ansible_collections.vmware.vcf.plugins.module_utils.basic import AnsibleModule
from plugins.modules.sddc_manager_nsxt_edge_cluster import EdgeClusterManager, VcfAPIException

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
def module_params():
    return {
        'sddc_manager_ip': '192.168.1.1',
        'sddc_manager_user': 'admin',
        'sddc_manager_password': 'password',
        'state': 'create',
        'validate': True,
        'management_cluster_name': 'management-cluster',
        'edge_cluster_payload': {
            'edgeNodeSpecs': [{'name': 'edge-node-1'}, {'name': 'edge-node-2'}]
        }
    }

@pytest.fixture
def ansible_module(module_params):
    module = Mock(spec=AnsibleModule)
    module.params = module_params
    return module

@pytest.fixture
def edge_cluster_manager(ansible_module):
    return EdgeClusterManager(ansible_module)

def test_get_host_cluster_by_name(mocker, edge_cluster_manager):
    mock_api_client = mocker.patch('plugins.modules.sddc_manager_nsxt_edge_cluster.SddcManagerApiClient')
    mock_api_client.return_value.get_clusters_all_clusters.return_value.data = {
        'elements': [{'name': 'management-cluster', 'id': 'cluster-id-1'}]
    }
    result = edge_cluster_manager.get_host_cluster_by_name('management-cluster')
    assert result['name'] == 'management-cluster'
    assert result['id'] == 'cluster-id-1'

def test_get_edge_cluster_by_name(mocker, edge_cluster_manager):
    mock_api_client = mocker.patch('plugins.modules.sddc_manager_nsxt_edge_cluster.SddcManagerApiClient')
    mock_api_client.return_value.get_edge_clusters.return_value.data = {
        'elements': [{'name': 'edge-cluster', 'id': 'edge-cluster-id-1'}]
    }
    result = edge_cluster_manager.get_edge_cluster_by_name('edge-cluster')
    assert result['name'] == 'edge-cluster'
    assert result['id'] == 'edge-cluster-id-1'

def test_create(mocker, edge_cluster_manager):
    mock_api_client = mocker.patch('plugins.modules.sddc_manager_nsxt_edge_cluster.SddcManagerApiClient')
    mock_api_client.return_value.create_edge_cluster.return_value.data = {
        'id': 'new-edge-cluster-id'
    }
    result = edge_cluster_manager.create()
    assert result['id'] == 'new-edge-cluster-id'

def test_create_with_exception(mocker, edge_cluster_manager):
    mock_api_client = mocker.patch('plugins.modules.sddc_manager_nsxt_edge_cluster.SddcManagerApiClient')
    mock_api_client.return_value.create_edge_cluster.side_effect = VcfAPIException("API Error")
    with pytest.raises(SystemExit):
        edge_cluster_manager.create()
    edge_cluster_manager.module.fail_json.assert_called_with(msg="Error: API Error")