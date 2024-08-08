from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vcf.plugins.module_utils.cloud_builder import CloudBuilderApiClient, VcfAPIException

class CloudBuilderValidationStatus:
    def __init__(self, module):
        self.module = module
        self.cloud_builder_ip = module.params['cloud_builder_ip']
        self.tasks_id = module.params['tasks_id']
        self.cloud_builder_user = module.params['cloud_builder_user']
        self.cloud_builder_password = module.params['cloud_builder_password']
        self.validation = module.params['validation']
        self.cloud_builder_tasks_type = module.params['cloud_builder_tasks_type']
        self.api_client = CloudBuilderApiClient(self.cloud_builder_ip, self.cloud_builder_user, self.cloud_builder_password)

    def evaluate_validation_status(self, payload_data):
        validation_check_list = payload_data['validationChecks']
        error_check_list = [check for check in validation_check_list if check['resultStatus'] == 'FAILED']
        if error_check_list:
            self.module.fail_json(changed=False, meta=error_check_list)
        else:
            self.module.exit_json(changed=False, meta=payload_data) #update to /home/segadson/.ansible/collections/ansible_collections/vmware/vcf/plugins/modules/cloud_builder_create_management_domain.py

    def process_validation_task(self, api_call_method):
        try:
            api_response = api_call_method(self.tasks_id)
            payload_data = api_response.data
            self.evaluate_validation_status(payload_data)
        except VcfAPIException as e:
            self.module.fail_json(changed=False, meta=str(e))

    def process_tasks(self):
        if self.validation:
            method_mapping = {
                'sddc_management_domain': self.api_client.get_sddc_validation
            }
            api_call_method = method_mapping.get(self.cloud_builder_tasks_type)
            if api_call_method:
                self.process_validation_task(api_call_method)
            else:
                self.module.fail_json(changed=False, msg="Invalid Tasks To Monitor")
        else:
            self.process_non_validation_task()

    def process_non_validation_task(self):
        try:
            api_response = self.api_client.get_sddc(self.tasks_id)
            payload_data = api_response.data
            self.evaluate_tasks_status(payload_data)
        except VcfAPIException as e:
            self.module.fail_json(changed=False, meta=str(e))

    @staticmethod
    def run():
        parameters = {
            "cloud_builder_ip": {"required": True, "type": "str"},
            "tasks_id": {"required": True, "type": "str"},
            "cloud_builder_user": {"required": True, "type": "str"},
            "cloud_builder_password": {"required": True, "type": "str", "no_log": True},
            "validation": {"type": "bool", "required": True},
            "cloud_builder_tasks_type": {
                "required": True, 
                "type": "str",
                "choices": ['sddc_management_domain']
            }
        }
        module = AnsibleModule(supports_check_mode=True, argument_spec=parameters)
        processor = CloudBuilderValidationStatus(module)
        processor.process_tasks()

if __name__ == '__main__':
    CloudBuilderValidationStatus.run()