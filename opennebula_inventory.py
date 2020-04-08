#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Hamid Yousefi <contact@hamidyousefi.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

EXAMPLES = '''
- name: create yaml formatted inventory file from opennebula hosted virtual machines
  opennebula_inventory:
    api: "https://domain.tld:2633/RPC2"
    username: opennebula-username
    password: opennebula-password
    dest: /tmp/inventory.yaml
'''

import pyone
import yaml
from jinja2 import Environment, BaseLoader
from ansible.module_utils.basic import AnsibleModule
from io import StringIO


class OpenNebulaInventoryCreator:
    @staticmethod
    def load_yaml(s):
        return yaml.load(StringIO(s))

    def __init__(self, config):
        self.classification = {}
        self.socket = None
        self.config = config

    def get_vm_list(self):
        if self.socket is None:
            socket = pyone.OneServer(
                self.config['api'],
                session="{}:{}".format(self.config['username'], self.config['password'])
            )

            self.socket = socket.vmpool.info(-2, -1, -1, -1)

        return self.socket.VM

    @staticmethod
    def get_ip(context):
        ip = context.get("ETH0_IP")

        if ip is None:
            ip = context.get("ETH4_IP")

        if ip is None:
            ip = context.get("ETH2_IP")

        return ip

    @staticmethod
    def get_labels(context):
        labels = context.get("LABELS")

        if labels is None or labels == "":
            return None

        return [label.strip() for label in labels.split(',')]

    def vm_classification(self):
        classification = {}
        vm_pool = []

        for vm in self.get_vm_list():
            ip = self.get_ip(vm.TEMPLATE["CONTEXT"])
            labels = self.get_labels(vm.USER_TEMPLATE)

            if ip is None or labels is None:
                continue

            for label in labels:
                if label not in classification:
                    classification[label] = []

                exists_in_classification = False
                for existed_vm_in_classification in classification[label]:
                    if ip == existed_vm_in_classification['ip']:
                        exists_in_classification = True
                        break

                vm_instance = {
                    'hostname': vm.NAME.strip(),
                    'ip': ip,
                    'port': 22
                }

                if not exists_in_classification:
                    classification[label].append(vm_instance)

                if not any(iterative_vm['ip'] == vm_instance['ip'] for iterative_vm in vm_pool):
                    vm_pool.append(vm_instance)

        return vm_pool, classification

    def template(self):
        template = """---
all:
  hosts:
    {%- for vm in vm_pool %}
    {{ vm.hostname }}:
      ansible_host: {{ vm.ip }}
      ansible_port: {{ vm.port }}
    {%- endfor %}

  children:
    {%- for label in classification %}
    {{ label }}:
      hosts:
        {%- for vm in classification[label] %}
        {{ vm.hostname }}:
        {%- endfor %}
    {%- endfor %}
        """

        vm_pool, classification = self.vm_classification()

        return Environment(loader=BaseLoader()).from_string(template).render(
            vm_pool=vm_pool,
            classification=classification
        )


def main():
    module_args = dict(
        api=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        dest=dict(type='str', required=True),
        static_src=dict(type='str', required=False)
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    result['changed'] = True

    if module.check_mode:
        module.exit_json(**result)

    with open(module.params['dest'], 'w') as destination:
        destination.write(OpenNebulaInventoryCreator(config=module.params).template())

    module.exit_json(**result)


if __name__ == '__main__':
    main()
