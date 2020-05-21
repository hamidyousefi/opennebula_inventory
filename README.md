# Ansible OpenNebula Inventory Module
In some circumstances you would like to generate your OpenNebula based inventory dynamically and keep the changes in a specific period.
This module will do it for you. simply create a playbook or write an Adhoc task somewhere in your workstation or controller machine
and execute it by schedule based job managers or crontab command. the file will be generated in the place you defined with the `dest` parameter. then you can use git or other mechanisms to keep the changes.


## Required Libraries
* PyOne
* YAML

## Setup
Copy `opennebula_inventory.py` into Ansible predefined modules path.

## Examples
```yaml
- name: create yaml formatted inventory file from opennebula hosted virtual machines
  opennebula_inventory:
    api: "https://domain.tld:2633/RPC2"
    username: opennebula-username
    password: opennebula-password
    dest: /tmp/inventory.yaml
```
