
import requests
import requests.packages
import json
from json import JSONDecodeError
import logging
from typing import List, Dict, Optional

def get_sddc_manager_token(url, sddc_manager_user, sddc_manager_password) -> str:
    main_url = url
    sddc_manager_url = "https://sddc-manager.vcf.sddc.lab/v1/tokens"#f"{main_url}/tokens"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "username": sddc_manager_user,
        "password": sddc_manager_password
    }
    try:
        response = requests.post(url=sddc_manager_url, headers=headers, json=payload, verify=False)
        print(response)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return None
    
url = "https://sddc-manager.vcf.sddc.lab/v1"
sddc_manager_user = "administrator@vsphere.local"
sddc_manager_password = "VMware123!"

get_sddc_manager_token(url, sddc_manager_user, sddc_manager_password)

response = requests.get(url="https://sddc-manager.vcf.sddc.lab/v1/clusters", headers={"Content-Type": "application/json"}, verify=False)