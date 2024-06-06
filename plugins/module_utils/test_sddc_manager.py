import unittest
from unittest.mock import MagicMock
from sddc_manager import SddcManagerApiClient
import unittest
from unittest.mock import MagicMock
from sddc_manager import SddcManagerApiClient

class TestSddcManagerApiClient(unittest.TestCase):

    def setUp(self):
        self.api_client = SddcManagerApiClient("sddc_manager_ip", "sddc_manager_user", "sddc_manager_password")

    def test_get_sddc_manager_token(self):
        # Mock the requests library
        self.api_client.get_sddc_manager_token = MagicMock(return_value={
            "status_code": 200,
            "message": "Success",
            "data": {
                "accessToken": "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNTFlZWI5Yy1mNWNmLTQ3N2UtYTJhYS0yMzg4ZmFmYzMwNDAiLCJpYXQiOjE1ODIxMzgzMzQsInN1YiI6ImFkbWluaXN0cmF0b3JAdnNwaGVyZS5sb2NhbCIsImlzcyI6InZjZi1hdXRoIiwiYXVkIjoic2RkYy1zZXJ2aWNlcyIsIm5iZiI6MTU4MjEzODMzNCwiZXhwIjoxNTgyMTQxOTM0LCJ1c2VyIjoiYWRtaW5pc3RyYXRvckB2c3BoZXJlLmxvY2FsIiwibmFtZSI6ImFkbWluaXN0cmF0b3JAdnNwaGVyZS5sb2NhbCIsInNjb3BlIjpbIkJBQ0tVUF9DT05GSUdfUkVBRCIsIkNSRURFTlRJQUxfUkVBRCIsIlVTRVJfV1JJVEUiLCJPVEhFUl9XUklURSIsIkJBQ0tVUF9DT05GSUdfV1JJVEUiLCJPVEhFUl9SRUFEIiwiVVNFUl9SRUFEIiwiQ1JFREVOVElBTF9XUklURSJdfQ.ylzrCyo4ymTKtSv1flmUrW-b8mxjRl7T2uV3a8sWWMA",
                "refreshToken": {
                    "id": "3c6b3c30-3bf2-480b-9539-8483699ab911"
                }
            }
        })

        # Call the method under test
        result = self.api_client.get_sddc_manager_token()

        # Assert the expected result
        self.assertEqual(result, {"status_code": 200, "message": "Success", "data": {
            "status_code": 200,
            "message": "Success",
            "data": {
                "accessToken": "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNTFlZWI5Yy1mNWNmLTQ3N2UtYTJhYS0yMzg4ZmFmYzMwNDAiLCJpYXQiOjE1ODIxMzgzMzQsInN1YiI6ImFkbWluaXN0cmF0b3JAdnNwaGVyZS5sb2NhbCIsImlzcyI6InZjZi1hdXRoIiwiYXVkIjoic2RkYy1zZXJ2aWNlcyIsIm5iZiI6MTU4MjEzODMzNCwiZXhwIjoxNTgyMTQxOTM0LCJ1c2VyIjoiYWRtaW5pc3RyYXRvckB2c3BoZXJlLmxvY2FsIiwibmFtZSI6ImFkbWluaXN0cmF0b3JAdnNwaGVyZS5sb2NhbCIsInNjb3BlIjpbIkJBQ0tVUF9DT05GSUdfUkVBRCIsIkNSRURFTlRJQUxfUkVBRCIsIlVTRVJfV1JJVEUiLCJPVEhFUl9XUklURSIsIkJBQ0tVUF9DT05GSUdfV1JJVEUiLCJPVEhFUl9SRUFEIiwiVVNFUl9SRUFEIiwiQ1JFREVOVElBTF9XUklURSJdfQ.ylzrCyo4ymTKtSv1flmUrW-b8mxjRl7T2uV3a8sWWMA",
                "refreshToken": {
                    "id": "3c6b3c30-3bf2-480b-9539-8483699ab911"
                }
            }
        }})
        self.api_client.get_sddc_manager_token.assert_called_once()

    def test_get_sddc_manager_token_failure(self):
        # Mock the requests library
        self.api_client.get_sddc_manager_token = MagicMock(return_value={"status_code": 400, "message": "Failure", "data": {}})

        # Call the method under test
        result = self.api_client.get_sddc_manager_token()

        # Assert the expected result
        self.assertEqual(result, {"status_code": 400, "message": "Failure", "data": {}})
        self.api_client.get_sddc_manager_token.assert_called_once()

    def test_sddc_operations(self):
        # Mock the requests library
        self.api_client.get_sddc_manager_token = MagicMock(return_value={"status_code": 200, "message": "Success", "data": {"accessToken": "token"}})
        sddc_operations_mock = MagicMock()
        sddc_operations_mock.return_value = {"status_code": 200, "message": "Success", "data": {}}
        self.api_client.sddc_operations = sddc_operations_mock

        # Call the method under test
        result = self.api_client.sddc_operations("GET")

        # Assert the expected result
        self.assertEqual(result, {"status_code": 200, "message": "Success", "data": {}})
        self.api_client.get_sddc_manager_token.assert_called_once()
        self.api_client.sddc_operations.assert_called_once_with("GET", None)


    def test_get_sddc_manager_task_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"task": "data1"}])
        result = self.sddc_manager.get_sddc_manager_task_by_id("resource_id")
        self.assertEqual(result, [{"task": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_sddc_manager_task_by_id_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))

        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_sddc_manager_task_by_id("resource_id")

        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_all_sddc_manager_tasks(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"task": "data1"}])
        result = self.sddc_manager.get_all_sddc_manager_tasks()
        self.assertEqual(result, [{"task": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_all_sddc_manager_tasks_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))

        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_all_sddc_manager_tasks()

        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_cancel_sddc_manager_tasks(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"task": "data1"}])
        result = self.sddc_manager.cancel_sddc_manager_tasks("resource_id")
        self.assertEqual(result, [{"task": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_retry_sddc_manager_tasks(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"task": "data1"}])
        result = self.sddc_manager.retry_sddc_manager_tasks("resource_id")
        self.assertEqual(result, [{"task": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH")

    def test_cancel_sddc_manager_tasks_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))

        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.cancel_sddc_manager_tasks("resource_id")

        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_validate_edge_cluster(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"edge_cluster": "data1"}])
        result = self.sddc_manager.validate_edge_cluster("payload")
        self.assertEqual(result, [{"edge_cluster": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "payload")
    
    def test_validate_edge_cluster_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))

        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.validate_edge_cluster("payload")

        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "payload")

    def test_edge_cluster_validation_status(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"edge_cluster": "data1"}])
        result = self.sddc_manager.edge_cluster_validation_status("resource_id")
        self.assertEqual(result, [{"edge_cluster": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_edge_cluster_validation_status_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))

        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.edge_cluster_validation_status("resource_id")

        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")    

    def test_create_edge_cluster(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"edge_cluster": "data1"}])
        result = self.sddc_manager.create_edge_cluster("payload")
        self.assertEqual(result, [{"edge_cluster": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "payload")
        
    def test_create_edge_cluster_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.create_edge_cluster("payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "payload")

    def test_expand_or_shrink_edge_cluster(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"edge_cluster": "data1"}])
        result = self.sddc_manager.expand_or_shrink_edge_cluster("resource_id", "payload")
        self.assertEqual(result, [{"edge_cluster": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "resource_id", "payload")

    def test_get_edge_clusters(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"edge_cluster": "data1"}])
        result = self.sddc_manager.get_edge_clusters()
        self.assertEqual(result, [{"edge_cluster": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_expand_or_shrink_edge_cluster_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.expand_or_shrink_edge_cluster("resource_id", "payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "resource_id", "payload")

    def test_get_edge_clusters_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_edge_clusters()
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_edge_cluster_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"edge_cluster": "data1"}])
        result = self.sddc_manager.get_edge_cluster_by_id("resource_id")
        self.assertEqual(result, [{"edge_cluster": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")
        
    def test_get_edge_cluster_by_id_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_edge_cluster_by_id("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_avns(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"avn1": "data1"}])
        result = self.sddc_manager.get_avns()
        self.assertEqual(result, [{"avn1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_validate_avns(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"avn1": "data1"}])
        result = self.sddc_manager.validate_avns("avn_payload")
        self.assertEqual(result, [{"avn1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "avn_payload")

    def test_create_avns(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"avn1": "data1"}])
        result = self.sddc_manager.create_avns("avn_payload")
        self.assertEqual(result, [{"avn1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "avn_payload")

    def test_get_avns_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_avns()
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_validate_avns_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.validate_avns("avn_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "avn_payload")

    def test_create_avns_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.create_avns("avn_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "avn_payload")

    def test_get_network_pools(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.get_network_pools()
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_network_pool_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.get_network_pool_by_id("resource_id")
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_create_network_pools(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.create_network_pools("network_pool_payload")
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "network_pool_payload")

    def test_update_network_pools(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.update_network_pools("resource_id", "network_pool_payload")
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "network_pool_payload")

    def test_delete_network_pools(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.delete_network_pools("resource_id")
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_network_pools_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_network_pools()
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_network_pool_by_id_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_network_pool_by_id("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_create_network_pools_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.create_network_pools("network_pool_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "network_pool_payload")

    def test_update_network_pools_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.update_network_pools("resource_id", "network_pool_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "network_pool_payload")

    def test_delete_network_pools_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.delete_network_pools("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_all_hosts(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"host1": "data1"}])
        result = self.sddc_manager.get_all_hosts()
        self.assertEqual(result, [{"host1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_host_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"host1": "data1"}])
        result = self.sddc_manager.get_host_by_id("resource_id")
        self.assertEqual(result, [{"host1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_hosts_by_status(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"host1": "data1"}])
        result = self.sddc_manager.get_hosts_by_status("UNASSIGNED_USEABLE")
        self.assertEqual(result, [{"host1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_validate_hosts(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"host1": "data1"}])
        result = self.sddc_manager.validate_hosts("host_payload")
        self.assertEqual(result, [{"host1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "host_payload")

    def test_commission_hosts(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"host1": "data1"}])
        result = self.sddc_manager.commission_hosts("host_payload")
        self.assertEqual(result, [{"host1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "host_payload")

    def test_decommission_hosts(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"host1": "data1"}])
        result = self.sddc_manager.decommission_hosts()
        self.assertEqual(result, [{"host1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_all_hosts_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_all_hosts()
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_host_by_id_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_host_by_id("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_hosts_by_status_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_hosts_by_status("UNASSIGNED_USEABLE")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_validate_hosts_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.validate_hosts("host_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "host_payload")

    def test_commission_hosts_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.commission_hosts("host_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "host_payload")

    def test_decommission_hosts_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.decommission_hosts()
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_clusters_all_clusters(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"cluster1": "data1"}])
        result = self.sddc_manager.get_clusters_all_clusters()
        self.assertEqual(result, [{"cluster1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_cluster_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"cluster1": "data1"}])
        result = self.sddc_manager.get_cluster_by_id("resource_id")
        self.assertEqual(result, [{"cluster1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_validate_clusters(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"cluster1": "data1"}])
        result = self.sddc_manager.validate_clusters("cluster_payload")
        self.assertEqual(result, [{"cluster1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "cluster_payload")

    def test_create_clusters(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"cluster1": "data1"}])
        result = self.sddc_manager.create_clusters("cluster_payload")
        self.assertEqual(result, [{"cluster1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "cluster_payload")

    def test_update_cluster(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"cluster1": "data1"}])
        result = self.sddc_manager.update_cluster("resource_id", "cluster_payload")
        self.assertEqual(result, [{"cluster1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "resource_id", "cluster_payload")

    def test_get_clusters_all_clusters_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_clusters_all_clusters()
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_cluster_by_id_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_cluster_by_id("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_validate_clusters_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.validate_clusters("cluster_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "cluster_payload")

    def test_create_clusters_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.create_clusters("cluster_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "cluster_payload")

    def test_update_cluster_failure(self):
        # Mock the sddc_operations method to raise an exception
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        # Call the method under test and assert that an exception is raised
        with self.assertRaises(Exception) as context:
            self.sddc_manager.update_cluster("resource_id", "cluster_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "resource_id", "cluster_payload")

    def test_get_network_pools(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.get_network_pools()
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_network_pool_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.get_network_pool_by_id("resource_id")
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_create_network_pools(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.create_network_pools("network_pool_payload")
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "network_pool_payload")

    def test_update_network_pools(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.update_network_pools("resource_id", "network_pool_payload")
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "network_pool_payload")

    def test_delete_network_pools(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"network_pool1": "data1"}])
        result = self.sddc_manager.delete_network_pools("resource_id")
        self.assertEqual(result, [{"network_pool1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_network_pools_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_network_pools()
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_network_pool_by_id_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_network_pool_by_id("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_create_network_pools_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.create_network_pools("network_pool_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "network_pool_payload")

    def test_update_network_pools_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.update_network_pools("resource_id", "network_pool_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "network_pool_payload")

    def test_delete_network_pools_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.delete_network_pools("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_all_domains(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"domain1": "data1"}])
        result = self.sddc_manager.get_all_domains()
        self.assertEqual(result, [{"domain1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_domain_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"domain1": "data1"}])
        result = self.sddc_manager.get_domain_by_id("resource_id")
        self.assertEqual(result, [{"domain1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_validate_domains(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"domain1": "data1"}])
        result = self.sddc_manager.validate_domains("domain_payload")
        self.assertEqual(result, [{"domain1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "domain_payload")

    def test_create_domains(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"domain1": "data1"}])
        result = self.sddc_manager.create_domains("domain_payload")
        self.assertEqual(result, [{"domain1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "domain_payload")

    def test_update_domains(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"domain1": "data1"}])
        result = self.sddc_manager.update_domains("resource_id", "domain_payload")
        self.assertEqual(result, [{"domain1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "domain_payload")

    def test_delete_domains(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"domain1": "data1"}])
        result = self.sddc_manager.delete_domains("resource_id")
        self.assertEqual(result, [{"domain1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_all_domains_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_all_domains()
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_domain_by_id_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_domain_by_id("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_validate_domains_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.validate_domains("domain_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "domain_payload")

    def test_create_domains_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.create_domains("domain_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "domain_payload")

    def test_update_domains_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.update_domains("resource_id", "domain_payload")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "domain_payload")

    def test_delete_domains_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.delete_domains("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_sddc_manager_upgrades(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"upgrade1": "data1"}])
        result = self.sddc_manager.get_sddc_manager_upgrades()
        self.assertEqual(result, [{"upgrade1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_sddc_manager_upgrade_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"upgrade1": "data1"}])
        result = self.sddc_manager.get_sddc_manager_upgrade_by_id("resource_id")
        self.assertEqual(result, [{"upgrade1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_perform_sddc_manager_upgrade_prechecks(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"upgrade1": "data1"}])
        result = self.sddc_manager.perform_sddc_manager_upgrade_prechecks("resource_id", "sddc_manager_payload")
        self.assertEqual(result, [{"upgrade1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "sddc_manager_payload")

    def test_get_sddc_manager_precheck_details(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"upgrade1": "data1"}])
        result = self.sddc_manager.get_sddc_manager_precheck_details("resource_id", "precheck_id")
        self.assertEqual(result, [{"upgrade1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_perform_sddc_manager_upgrade(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"upgrade1": "data1"}])
        result = self.sddc_manager.perform_sddc_manager_upgrade("sddc_manager_payload")
        self.assertEqual(result, [{"upgrade1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "sddc_manager_payload")

    def test_commit_reschedule_sddc_manager_upgrade(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"upgrade1": "data1"}])
        result = self.sddc_manager.commit_reschedule_sddc_manager_upgrade("resource_id", "sddc_manager_payload")
        self.assertEqual(result, [{"upgrade1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "sddc_manager_payload")

    def test_get_sddc_manager_upgrades_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_sddc_manager_upgrades()
        self.assertTrue('An error occurred' in str(context.exception))

    def test_get_sddc_manager_upgrade_by_id_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_sddc_manager_upgrade_by_id("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_perform_sddc_manager_upgrade_prechecks_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.perform_sddc_manager_upgrade_prechecks("resource_id", "sddc_manager_payload")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_get_sddc_manager_precheck_details_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_sddc_manager_precheck_details("resource_id", "precheck_id")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_perform_sddc_manager_upgrade_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.perform_sddc_manager_upgrade("sddc_manager_payload")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_commit_reschedule_sddc_manager_upgrade_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.commit_reschedule_sddc_manager_upgrade("resource_id", "sddc_manager_payload")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_get_all_vasa_providers(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"provider1": "data1"}])
        result = self.sddc_manager.get_all_vasa_providers()
        self.assertEqual(result, [{"provider1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_vasa_provider_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"provider1": "data1"}])
        result = self.sddc_manager.get_vasa_provider_by_id("resource_id")
        self.assertEqual(result, [{"provider1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_validate_vasa_provider(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"provider1": "data1"}])
        result = self.sddc_manager.validate_vasa_provider("vasa_provider_payload")
        self.assertEqual(result, [{"provider1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "vasa_provider_payload")

    def test_create_vasa_provider(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"provider1": "data1"}])
        result = self.sddc_manager.create_vasa_provider("vasa_provider_payload")
        self.assertEqual(result, [{"provider1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "vasa_provider_payload")

    def test_update_vasa_provider(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"provider1": "data1"}])
        result = self.sddc_manager.update_vasa_provider("resource_id", "vasa_provider_payload")
        self.assertEqual(result, [{"provider1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("PATCH", "vasa_provider_payload")

    def test_delete_vasa_provider(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"provider1": "data1"}])
        result = self.sddc_manager.delete_vasa_provider("resource_id")
        self.assertEqual(result, [{"provider1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_all_vasa_providers_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_all_vasa_providers()
        self.assertTrue('An error occurred' in str(context.exception))

    def test_get_vasa_provider_by_id_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_vasa_provider_by_id("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_validate_vasa_provider_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.validate_vasa_provider("vasa_provider_payload")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_create_vasa_provider_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.create_vasa_provider("vasa_provider_payload")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_update_vasa_provider_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.update_vasa_provider("resource_id", "vasa_provider_payload")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_delete_vasa_provider_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.delete_vasa_provider("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_get_vsas_provider_storage_containers(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"container1": "data1"}])
        result = self.sddc_manager.get_vsas_provider_storage_containers("resource_id")
        self.assertEqual(result, [{"container1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_add_vsas_provider_storage_containters(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"container1": "data1"}])
        result = self.sddc_manager.add_vsas_provider_storage_containters("resource_id", "payload")
        self.assertEqual(result, [{"container1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "payload")

    def test_delete_vasa_provider_stroage_container(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"container1": "data1"}])
        result = self.sddc_manager.delete_vasa_provider_stroage_container("resource_id", "container_id")
        self.assertEqual(result, [{"container1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_get_vsas_provider_users(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"user1": "data1"}])
        result = self.sddc_manager.get_vsas_provider_users("resource_id")
        self.assertEqual(result, [{"user1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_add_vsas_provider_users(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"user1": "data1"}])
        result = self.sddc_manager.add_vsas_provider_users("resource_id", "payload")
        self.assertEqual(result, [{"user1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "payload")

    def test_get_vsas_provider_storage_containers_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_vsas_provider_storage_containers("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_add_vsas_provider_storage_containters_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.add_vsas_provider_storage_containters("resource_id", "payload")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_delete_vasa_provider_stroage_container_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.delete_vasa_provider_stroage_container("resource_id", "container_id")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_get_vsas_provider_users_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_vsas_provider_users("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_add_vsas_provider_users_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.add_vsas_provider_users("resource_id", "payload")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_get_all_lifecycle_manager_images(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"image1": "data1"}])
        result = self.sddc_manager.get_all_lifecycle_manager_images()
        self.assertEqual(result, [{"image1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_upload_life_cycle_manager_image(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"image1": "data1"}])
        result = self.sddc_manager.upload_life_cycle_manager_image("payload")
        self.assertEqual(result, [{"image1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "payload")

    def test_get_lifecycle_manager_image_by_id(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"image1": "data1"}])
        result = self.sddc_manager.get_lifecycle_manager_image_by_id("resource_id")
        self.assertEqual(result, [{"image1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_get_lifecycle_manager_image_by_name(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"image1": "data1"}])
        result = self.sddc_manager.get_lifecycle_manager_image_by_name("image_name")
        self.assertEqual(result, [{"image1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("GET")

    def test_delete_lifecycle_manager_image(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"image1": "data1"}])
        result = self.sddc_manager.delete_lifecycle_manager_image("resource_id")
        self.assertEqual(result, [{"image1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("DELETE")

    def test_upload_lifecycle_image_files(self):
        self.sddc_manager.sddc_operations = MagicMock(return_value=[{"image1": "data1"}])
        result = self.sddc_manager.upload_lifecycle_image_files("payload")
        self.assertEqual(result, [{"image1": "data1"}])
        self.sddc_manager.sddc_operations.assert_called_once_with("POST", "payload")

    def test_get_all_lifecycle_manager_images_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_all_lifecycle_manager_images()
        self.assertTrue('An error occurred' in str(context.exception))

    def test_upload_life_cycle_manager_image_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.upload_life_cycle_manager_image("payload")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_get_lifecycle_manager_image_by_id_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_lifecycle_manager_image_by_id("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_get_lifecycle_manager_image_by_name_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.get_lifecycle_manager_image_by_name("image_name")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_delete_lifecycle_manager_image_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.delete_lifecycle_manager_image("resource_id")
        self.assertTrue('An error occurred' in str(context.exception))

    def test_upload_lifecycle_image_files_failure(self):
        self.sddc_manager.sddc_operations = MagicMock(side_effect=Exception("An error occurred"))
        with self.assertRaises(Exception) as context:
            self.sddc_manager.upload_lifecycle_image_files("payload")
        self.assertTrue('An error occurred' in str(context.exception))
        '''
        To Do:
        - Add the Rest of the test cases 
        - Add Responses
class SomeClass:
    def some_method(self, value):
        pass  # some implementation

class TestSomeClass(unittest.TestCase):
    def setUp(self):
        self.some_object = SomeClass()

    def test_some_method_returns_different_values(self):
        self.some_object.some_method = MagicMock(side_effect=[1, 2, 3])
        self.assertEqual(self.some_object.some_method(), 1)
        self.assertEqual(self.some_object.some_method(), 2)
        self.assertEqual(self.some_object.some_method(), 3)

        '''
if __name__ == '__main__':
    unittest.main()