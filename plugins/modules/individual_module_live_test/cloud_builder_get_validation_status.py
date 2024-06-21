#!/usr/bin/env python
import json
from ansible.module_utils.basic import AnsibleModule
from cloud_builder_get_validation_status import CloudBuilderGetValidationStatus


# chmod +x test_module.py
# ./test_module.py '{"cloud_builder_ip": "192.168.1.100", "sddc_id": "sddc-123"}'`

def main():
    # Define the arguments in the same way they are defined in the module
    module_args = dict(
        cloud_builder_ip=dict(type='str', required=True),
        sddc_id=dict(type='str', required=True)
    )

    # Instantiate the AnsibleModule class with the defined arguments
    module = AnsibleModule(argument_spec=module_args)

    # Create an instance of your module class here (modify as necessary)
    # Assuming CloudBuilderGetValidationStatus is the class name inside your module
    # and it takes these arguments in its constructor or has a method to set them
    instance = CloudBuilderGetValidationStatus(module.params['cloud_builder_ip'], module.params['sddc_id'])

    # Assuming your class has a method named 'run' to execute the main functionality
    # Modify this part according to how your module is structured
    result = instance.run()

    # Exiting the module, returning the result
    module.exit_json(**result)

if __name__ == '__main__':
    main()

# To test the module, you can run the following command:
# chmod +x test_module.py
# ./test_module.py '{"cloud_builder_ip": "192.168.1.100", "sddc_id": "sddc-123"}'`