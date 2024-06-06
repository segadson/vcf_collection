import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import requests
import requests.packages
import json
from json import JSONDecodeError
import logging
from typing import List, Dict
from module_utils.exceptions import VcfAPIException
from module_utils.outputs import Result

class CloudBuilderApiClient:

    #Todo - Add Self.id

    def __init__(self, cloud_builder_ip: str, cloud_builder_user: str, cloud_builder_password: str, ssl_verify: bool = False, logger: logging.Logger = None, sddc_manager_api_string: str = None, validations: bool = False):
        self.cloud_builder_ip = cloud_builder_ip
        self.cloud_builder_user = cloud_builder_user
        self.cloud_builder_password = cloud_builder_password
        self.sddc_manager_api_string = sddc_manager_api_string
        self.validations = validations
        self.logger = logger or logging.getLogger(__name__)
        self.ssl_verify = ssl_verify
        if not self.ssl_verify:
            requests.packages.urllib3.disable_warnings()

#To Do- Defensive Programming CHeck for self params and raise exception if not set

    #######################################
    # Cloud Builder perations
    #######################################


    def sddc_operations(self, http_method: str, sddc_id: str = None, sddc_management_domain_payload: str = None):


        if self.validations == True:
            udpated_url = f"https://{self.cloud_builder_ip}/v1/{self.sddc_manager_api_string}/validations"
        else:
            udpated_url = f"https://{self.cloud_builder_ip}/v1/{self.sddc_manager_api_string}"

        if sddc_id:
            udpated_url = f"https://{self.cloud_builder_ip}/v1/sddcs/{sddc_id}"

        else:
            udpated_url = f"https://{self.cloud_builder_ip}/v1/sddcs/"
        if sddc_id:
            cloud_builder_url = f"{udpated_url}/{sddc_id}"

        else:
            cloud_builder_url = f"{udpated_url}/"
        
        headers = {
            "Content-Type": "application/json"
        }

        log_line_pre = f"method={http_method}, url={cloud_builder_url}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))
        
        try:
            self.logger.debug(log_line_pre)
            response = requests.request(method=http_method, url=cloud_builder_url, headers=headers, auth=(self.cloud_builder_user, self.cloud_builder_password), 
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
    
    
    def get_sddc(self,  sddc_id: str = None) -> List[Dict]:
        self.sddc_manager_api_string = "sddcs"
        self.validations = False
        return self.sddc_operations("GET",  sddc_id)
    
    def create_sddc(self, sddc_id: str = None,  sddc_management_domain_payload: str = None) -> Dict:
        self.sddc_manager_api_string = "sddcs"
        self.validations = False
        return self.sddc_operations("POST", sddc_id,  sddc_management_domain_payload)
    
    # def delete_sddc(self,  sddc_management_domain_payload: str = None) -> Dict:
    #     return self.sddc_operations("DELETE",  sddc_management_domain_payload)
    
    def retry_sddc(self, sddc_id: str = None ,sddc_management_domain_payload: str = None) -> Dict:
        self.sddc_manager_api_string = "sddcs"
        self.validations = False
        return self.sddc_operations("PATCH",  sddc_id, sddc_management_domain_payload)

    #######################################
    # Cloud Builder Validations Operations
    #######################################
    
    def get_sddc_validation(self, sddc_id: str = None) -> List[Dict]:
        self.sddc_manager_api_string = "sddcs"
        self.validations = True
        return self.sddc_validation_operations("GET", sddc_id)
    
    def validate_sddc(self,  sddc_id: str = None, sddc_management_domain_payload: str = None) -> Dict:
        self.sddc_manager_api_string = "sddcs"
        self.validations = True
        return self.sddc_validation_operations("POST", sddc_id, sddc_management_domain_payload)
    
    #Todo - Add Params for which Validation or build failed? 
    def retry_sddc_validation(self, sddc_id: str = None, sddc_management_domain_payload: str = None) -> Dict:
        self.sddc_manager_api_string = "sddcs"
        self.validations = True
        return self.sddc_validation_operations("PATCH", sddc_id ,sddc_management_domain_payload)
    
    