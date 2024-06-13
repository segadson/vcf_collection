
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

    # def print_dict_diff(dict1, dict2, path=""):
    #     for key in dict1.keys():
    #         if key in dict2:
    #             if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
    #                 print_dict_diff(dict1[key], dict2[key], path + str(key) + " -> ")
    #             elif dict1[key] == dict2[key]:
    #                 pass
    #             else:
    #                 print("Key:", path + str(key))
    #                 print("Dict1 value:", dict1[key])
    #                 print("Dict2 value:", dict2[key])
    #                 print("---")
    #         else:
    #             print("Key:", path + str(key))
    #             print("Dict1 value:", dict1[key])
    #             print("Dict2 value: Does not exist")
    #             print("---")

    #     for key in dict2.keys():
    #         if key not in dict1:
    #             print("Key:", path + str(key))
    #             print("Dict1 value: Does not exist")
    #             print("Dict2 value:", dict2[key])
    #             print("---")
        #module.log(msg=f"Workload Domain Payload: {json.dumps(updated_workload_domain_payload)}")
        # print_dict_diff(updated_workload_domain_payload, correct_payload)    
        # stop