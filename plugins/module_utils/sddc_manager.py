import os
import sys


# current_dir = os.path.dirname(os.path.realpath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

import requests
import requests.packages
import json
from json import JSONDecodeError
import logging
from typing import List, Dict, Optional
from ansible.module_utils.exceptions import VcfAPIException
from ansible.module_utils.outputs import Result

class SddcManagerApiClient:
    """
    A client for interacting with the SDDC Manager API.

    Args:
        sddc_manager_ip (str): The IP address of the SDDC Manager.
        sddc_manager_user (str): The username for authenticating with the SDDC Manager.
        sddc_manager_password (str): The password for authenticating with the SDDC Manager.
        ssl_verify (bool, optional): Whether to verify the SSL certificate of the SDDC Manager. Defaults to False.
        logger (logging.Logger, optional): The logger to use for logging. Defaults to None.
        api_extension (str, optional): The API extension to use for making API requests. Defaults to None.

    Raises:
        VcfAPIException: If the API extension is not set.

    Attributes:
        sddc_manager_ip (str): The IP address of the SDDC Manager.
        sddc_manager_user (str): The username for authenticating with the SDDC Manager.
        sddc_manager_password (str): The password for authenticating with the SDDC Manager.
        api_extension (str): The API extension to use for making API requests.
        url (str): The URL of the SDDC Manager API.
        logger (logging.Logger): The logger to use for logging.
        ssl_verify (bool): Whether to verify the SSL certificate of the SDDC Manager.

    Methods:
        get_sddc_manager_token: Retrieves the access token for authenticating with the SDDC Manager.
        sddc_operations: Performs SDDC Manager operations by making API requests.
        get_sddc_manager_task_by_id: Retrieves a specific SDDC Manager task by its resource ID.
        get_all_sddc_manager_tasks: Retrieves all SDDC Manager tasks.
        cancel_sddc_manager_tasks: Cancels a specific SDDC Manager task by its resource ID.
        retry_sddc_manager_tasks: Retries a specific SDDC Manager task by its resource ID.
        validate_edge_cluster: Validates an edge cluster.
        edge_cluster_validation_status: Retrieves the validation status of an edge cluster.
        create_edge_cluster: Creates an edge cluster.
        expand_or_shrink_edge_cluster: Expands or shrinks an edge cluster.
        get_edge_clusters: Retrieves all edge clusters.
        get_edge_cluster_by_id: Retrieves a specific edge cluster by its resource ID.
        get_avns: Retrieves all AVNs (Application Virtual Networks).
        validate_avns: Validates AVNs.
        create_avns: Creates AVNs.
        get_network_pools: Retrieves all network pools.
        get_network_pool_by_id: Retrieves a specific network pool by its resource ID.
        create_network_pools: Creates network pools.
        update_network_pools: Updates a specific network pool by its resource ID.
        delete_network_pools: Deletes a specific network pool by its resource ID.
        get_all_hosts: Retrieves all hosts.
        get_host_by_id: Retrieves a specific host by its resource ID.
        get_hosts_by_status: Retrieves hosts by their status.
        validate_hosts: Validates hosts.
        commission_hosts: Commissions hosts.
        decommission_hosts: Decommissions hosts.
        get_clusters_all_clusters: Retrieves all clusters.
        get_cluster_by_id: Retrieves a specific cluster by its resource ID.
    """

    #Todo - Add Self.id

    def __init__(self, sddc_manager_ip: str, sddc_manager_user: str, sddc_manager_password: str, ssl_verify: bool = False, 
                 logger: logging.Logger = None): #, api_extension: str = None

        self.sddc_manager_ip = sddc_manager_ip
        self.sddc_manager_user = sddc_manager_user
        self.sddc_manager_password = sddc_manager_password
        #self.api_extension = api_extension
        self.url = f"https://{self.sddc_manager_ip}/v1"
        self.logger = logger or logging.getLogger(__name__)
        self.ssl_verify = ssl_verify
        if not self.ssl_verify:
            requests.packages.urllib3.disable_warnings()


    #To Do- Defensive Programming CHeck for self params and raise exception if not set

    def get_sddc_manager_token(self) -> str:
        main_url = self.url
        sddc_manager_url = f"{main_url}/tokens"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "username": self.sddc_manager_user,
            "password": self.sddc_manager_password
        }
        try:
            response = requests.post(url=sddc_manager_url, headers=headers, json=payload, verify=self.ssl_verify)
            print(f"Response: {response}")
            stop
        except requests.exceptions.RequestException as e:
            raise VcfAPIException(f"Error: {e}")    
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            raise VcfAPIException("Bad JSON in response") from e
        is_success = 299 >= response.status_code >= 200     # 200 to 299 is OK
        if is_success:
            return Result(response.status_code, message=response.reason, data=data_out)

        raise VcfAPIException(f"{response.status_code}: {response.reason}") 


    #######################################
    # SDDC Manager perations
    #######################################


    def sddc_operations(self, http_method: str, sddc_management_domain_payload: str = None):

        if sddc_management_domain_payload is not type(str):
            sddc_management_domain_payload = json.dumps(sddc_management_domain_payload)

        elif http_method in ["POST", "PATCH"] and sddc_management_domain_payload is None:
            raise VcfAPIException("Payload is required for POST or PATCH requests")

        #self.api_extension = api_extension
        sddc_manager_url = f"{self.url}/{self.api_extension}"
        
        ####################################
        # Get Token
        ####################################
        sddc_token_result= self.get_sddc_manager_token().data
        sddc_token = sddc_token_result['accessToken']
        headers = {
            "Content-Type": "application/json",
            'Authorization': f'Bearer {sddc_token}'
        }

        log_line_pre = f"method={http_method}, url={sddc_manager_url}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))
        
        try:
            self.logger.debug(log_line_pre)
            response = requests.request(method=http_method, url=sddc_manager_url, headers=headers,
                                        verify=self.ssl_verify,  data=sddc_management_domain_payload)

        except requests.exceptions.RequestException as e:
            self.logger.error(msg=(str(e)))
            raise VcfAPIException(f"Error: {e}")    

        try:
            data_out = response.json()

        except (ValueError, JSONDecodeError) as e:
            self.logger.error(msg=log_line_post.format(False, None, e))
            raise VcfAPIException("Bad JSON in response") from e
        is_success = 299 >= response.status_code >= 200     # 200 to 299 is OK
        log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if is_success:
            self.logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason, data=data_out)
        self.logger.error(msg=log_line)
        raise VcfAPIException(f"{response.status_code}: {response.reason}") #data_out
    
    #######################################
    # To do: Create Class for SDDC
    # https://app.quicktype.io/
    #######################################

    #################################################
    # SDDC Manager Tasks
    #################################################
    def get_sddc_manager_task_by_id(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"tasks/{resource_id}"
        return self.sddc_operations("GET")
    
    def get_all_sddc_manager_tasks(self) -> List[Dict]:
        self.api_extension = f"tasks"
        return self.sddc_operations("GET")
    
    def cancel_sddc_manager_tasks(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"tasks/{resource_id}"
        return self.sddc_operations("DELETE")
    
    def retry_sddc_manager_tasks(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"tasks/{resource_id}"
        return self.sddc_operations("PATCH")

    #################################################
    # Edge Cluster Operations
    #################################################

    def validate_edge_cluster(self,  edge_cluster_payload: str = None) -> List[Dict]:
        self.api_extension = f"edge-clusters/validations"
        return self.sddc_operations("POST",  edge_cluster_payload)

    def edge_cluster_validation_status(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"edge-clusters/validations/{resource_id}"
        return self.sddc_operations("GET")

    def create_edge_cluster(self, edge_cluster_payload: str = None) -> List[Dict]:
        self.api_extension = f"edge-clusters"
        return self.sddc_operations("POST", edge_cluster_payload)
        
    def expand_or_shrink_edge_cluster(self,  resource_id: str = None, edge_cluster_payload: str = None) -> List[Dict]:
        self.api_extension = f"edge-clusters/{resource_id}"
        return self.sddc_operations("PATCH",  resource_id, edge_cluster_payload)

    def get_edge_clusters(self) -> List[Dict]:
        self.api_extension = f"edge-clusters"
        return self.sddc_operations("GET")
    
    def get_edge_cluster_by_id(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = "edge-clusters/{resource_id}"
        return self.sddc_operations("GET")


    #################################################
    # AVN Operations
    #################################################
    def get_avns(self) -> List[Dict]:
        self.api_extension = f"avns"
        return self.sddc_operations("GET")
    def validate_avns(self,  avn_payload: str = None) -> List[Dict]:
        self.api_extension = f"avns/validations"
        return self.sddc_operations("POST",  avn_payload)
    def create_avns(self, avn_payload: str = None) -> List[Dict]:
        self.api_extension = f"avns"
        return self.sddc_operations("POST", avn_payload)
    
    #################################################
    # Network Pool Operations
    #################################################
    def get_network_pools(self) -> List[Dict]:
        self.api_extension = f"network-pools"
        return self.sddc_operations("GET")
    
    def get_network_pool_by_id(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"network-pools/{resource_id}"
        return self.sddc_operations("GET")

    def create_network_pools(self, network_pool_payload: str = None) -> List[Dict]:
        self.api_extension = f"network-pools"
        return self.sddc_operations("POST", network_pool_payload)
    
    def update_network_pools(self,  resource_id: str = None, network_pool_payload: str = None) -> List[Dict]:
        self.api_extension = f"network-pools/{resource_id}"
        return self.sddc_operations("PATCH", network_pool_payload)
    
    def delete_network_pools(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"network-pools/{resource_id}"
        return self.sddc_operations("DELETE")
    
    #################################################
    # Host Operations
    #################################################
    def get_all_hosts(self) -> List[Dict]:
        self.api_extension = f"hosts"
        return self.sddc_operations("GET")
    
    def get_host_by_id(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = "hosts/{resource_id}"
        return self.sddc_operations("GET")
    
    def get_hosts_by_status(self,  status: str = None) -> List[Dict]:
        '''
        Status can be one of the following:
        - UNASSIGNED_USEABLE
        - UNASSIGNED_UNUSEABLE
        - ASSIGNED
        '''
        self.api_extension = f"hosts?status={status}"
        return self.sddc_operations("GET")
    
    def validate_hosts(self, host_payload: str = None) -> List[Dict]:
        self.api_extension = f"hosts/validations"
        return self.sddc_operations("POST", host_payload)
    
    def commission_hosts(self, host_payload: str = None) -> List[Dict]:
        self.api_extension = f"hosts"
        return self.sddc_operations("POST", host_payload)
    
    def decommission_hosts(self) -> List[Dict]:
        self.api_extension = f"hosts"
        return self.sddc_operations("DELETE")
    
    #################################################
    # Cluster Operations
    #################################################
    def get_clusters_all_clusters(self) -> List[Dict]:
        self.api_extension = f"clusters"
        return self.sddc_operations("GET")

    def get_cluster_by_id(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"clusters/{resource_id}"
        return self.sddc_operations("GET")
    
    def validate_clusters(self, cluster_payload: str = None) -> List[Dict]:
        self.api_extension = f"clusters/validations"
        return self.sddc_operations("POST",cluster_payload)
    
    def create_clusters(self, cluster_payload: str = None) -> List[Dict]:
        self.api_extension = f"clusters"
        return self.sddc_operations("POST",  cluster_payload)
    
    def update_cluster(self,  resource_id: str = None, cluster_payload: str = None) -> List[Dict]:
        '''
        This Action Can either:
        - Add or Remove Hosts
        - Strecth or Unstrech Cluster
        '''
        self.api_extension = f"clusters/{resource_id}"
        return self.sddc_operations("PATCH",  resource_id, cluster_payload)
    
    def mount_datastore_on_cluster(self,  resource_id: str = None, cluster_payload: str = None) -> List[Dict]:
        self.api_extension = f"clusters/{resource_id}/datastores"
        return self.sddc_operations("POST",  cluster_payload)
    
    def validate_mount_datastore_on_cluster(self,  resource_id: str = None, cluster_payload: str = None) -> List[Dict]:
        self.api_extension = f"clusters/{resource_id}/datastores/validation"
        return self.sddc_operations("POST", cluster_payload)

    def unmount_datastore_on_cluster(self,  resource_id: str = None, datastoreId: str = None) -> List[Dict]:
        self.api_extension = f"clusters/{resource_id}/datastores/{datastoreId}"
        return self.sddc_operations("DELETE")
    
    def get_vsan_remote_hci_datastore_from_cluster(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"clusters/{resource_id}/datastores/criteria/VSAN_REMOTE_DATASTORES"
        return self.sddc_operations("GET")

    def delete_cluster(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"clusters/{resource_id}"
        return self.sddc_operations("DELETE")

    #################################################
    # Workload Domain Operations
    #################################################
    def get_all_domains(self) -> List[Dict]:
        self.api_extension = f"domains"
        self.validations = False
        return self.sddc_operations("GET")
    
    def get_domain_by_id(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"domains/{resource_id}"
        return self.sddc_operations("GET")
    
    def validate_domains(self, domain_payload: str = None) -> List[Dict]:
        self.api_extension = f"domains/validations"
        return self.sddc_operations("POST", domain_payload)

    def create_domains(self,domain_payload: str = None) -> List[Dict]:
        self.api_extension = f"domains"
        return self.sddc_operations("POST", domain_payload)
    
    def update_domains(self,  resource_id: str = None, domain_payload: str = None) -> List[Dict]:
        self.api_extension = f"domains/{resource_id}"
        return self.sddc_operations("PATCH", domain_payload)

    def delete_domains(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"domains/{resource_id}"
        return self.sddc_operations("DELETE")

    #################################################
    # SDDC Manager Upgrade Operations
    #################################################
    def get_sddc_manager_upgrades(self) -> List[Dict]:
        self.api_extension = f"upgrades"
        return self.sddc_operations("GET")
    
    def get_sddc_manager_upgrade_by_id(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"upgrades/{resource_id}"
        return self.sddc_operations("GET")

    def perform_sddc_manager_upgrade_prechecks(self, resource_id: str = None ,sddc_manager_payload: str = None) -> List[Dict]:
        self.api_extension = f"upgrades/{resource_id}/prechecks"
        return self.sddc_operations("POST", sddc_manager_payload)
    
    def get_sddc_manager_precheck_details(self,  resource_id: str = None, precheck_id: str = None) -> List[Dict]:
        self.api_extension = f"upgrades/{resource_id}/prechecks/{precheck_id}"
        return self.sddc_operations("GET")

    def perform_sddc_manager_upgrade(self,  sddc_manager_payload: str = None) -> List[Dict]:
        self.api_extension = f"upgrades"
        return self.sddc_operations("POST", sddc_manager_payload)
    
    def commit_reschedule_sddc_manager_upgrade(self,  resource_id: str = None, sddc_manager_payload: str = None) -> List[Dict]:
        self.api_extension = f"upgrades/{resource_id}"
        return self.sddc_operations("PATCH", sddc_manager_payload)

    #################################################
    # VASA Providers Operations
    #################################################
    def get_all_vasa_providers(self) -> List[Dict]:
        self.api_extension = f"vasa-providers"
        return self.sddc_operations("GET")
    
    def get_vasa_provider_by_id(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers/{resource_id}"
        return self.sddc_operations("GET")
    
    def validate_vasa_provider(self, vasa_provider_payload: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers/validations"
        return self.sddc_operations("POST", vasa_provider_payload)
    
    def create_vasa_provider(self, vasa_provider_payload: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers"
        return self.sddc_operations("POST", vasa_provider_payload)
    
    def update_vasa_provider(self,  resource_id: str = None, vasa_provider_payload: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers/{resource_id}"
        return self.sddc_operations("PATCH", vasa_provider_payload)
    
    def delete_vasa_provider(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers/{resource_id}"
        return self.sddc_operations("DELETE")
    
    def get_vsas_provider_storage_containers(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers/{resource_id}/storage-containers"
        return self.sddc_operations("GET")
    
    def add_vsas_provider_storage_containters(self,  resource_id: str = None, vasa_provider_stroage_containter_payload: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers/{resource_id}/storage-containers"
        return self.sddc_operations("POST", vasa_provider_stroage_containter_payload)
    
    def delete_vasa_provider_stroage_container(self,  resource_id: str = None, storage_container_id: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers/{resource_id}/storage-containers/{storage_container_id}"
        return self.sddc_operations("DELETE")
    
    def get_vsas_provider_users(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers/{resource_id}/users"
        return self.sddc_operations("GET")
    
    def add_vsas_provider_users(self,  resource_id: str = None, vasa_provider_user_payload: str = None) -> List[Dict]:
        self.api_extension = f"vasa-providers/{resource_id}/users"
        return self.sddc_operations("POST", vasa_provider_user_payload)

    #################################################
    # SDDC Manager Lifce Manger Image Operations
    #################################################
    def get_all_lifecycle_manager_images(self) -> List[Dict]:
        self.api_extension = f"personalities"
        return self.sddc_operations("GET")
    
    def upload_life_cycle_manager_image(self, lifecycle_manager_image_payload: str = None) -> List[Dict]:
        self.api_extension = f"personalities"
        return self.sddc_operations("POST", lifecycle_manager_image_payload)
    
    def get_lifecycle_manager_image_by_id(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"personalities/{resource_id}"
        return self.sddc_operations("GET")
    
    def get_lifecycle_manager_image_by_name(self,  image_name: str = None) -> List[Dict]:
        self.api_extension = f"personalities?personalityName={image_name}"
        return self.sddc_operations("GET")

    def delete_lifecycle_manager_image(self,  resource_id: str = None) -> List[Dict]:
        self.api_extension = f"personalities/{resource_id}"
        return self.sddc_operations("DELETE")

    def upload_lifecycle_image_files(self,  lifecycle_manager_image_payload: str = None) -> List[Dict]:
        self.api_extension = f"personalities/files"
        return self.sddc_operations("POST", lifecycle_manager_image_payload)

    
#################################################

# Test API Call
#################################################
# sddc_manager_ip = "sddc-manager.vcf.sddc.lab"
# sddc_manager_user = "administrator@vsphere.local"
# sddc_manager_password = "VMware123!"
# sddc_id = "aebf1dab-c650-4571-a5dc-7f7c72e61aa3"
# api_client = SddcManagerApiClient(sddc_manager_ip, sddc_manager_user, sddc_manager_password)
# api_response = api_client.get_sddc_domains(sddc_id)
# payload_data = api_response.data

# print(payload_data)