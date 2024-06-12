
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
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return None
    
url = "https://sddc-manager.vcf.sddc.lab/v1"
sddc_manager_user = "administrator@vsphere.local"
sddc_manager_password = "VMware123!"

return_value = get_sddc_manager_token(url, sddc_manager_user, sddc_manager_password)
token = return_value["accessToken"]

payload = {
    "avns": [ {
        "gateway": "10.50.0.1",
        "mtu": 8940,
        "name": "region-seg01",
        "regionType": "REGION_A",
        "routerName": "VLC-Tier-1",
        "subnet": "10.50.0.0",
        "subnetMask": "255.255.255.0"
    }, {
        "gateway": "10.60.0.1",
        "mtu": 8940,
        "name": "xregion-seg01",
        "regionType": "X_REGION",
        "routerName": "VLC-Tier-1",
        "subnet": "10.60.0.0",
        "subnetMask": "255.255.255.0"
    }],
    "edgeClusterId": "1.1.1.1"
}
response = requests.post(url="https://sddc-manager.vcf.sddc.lab/v1/avns/validations", headers={"Authorization": f"Bearer {token}"}, data=json.dumps(payload),verify=False)
print(response)