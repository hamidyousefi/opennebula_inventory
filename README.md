# Ansible OpenNebula Inventory Module

## Preface
When people talk about IaC, using one of the configuration management tools becomes inevitable. 
Depends on your needs and requirements, you may force to choose between them! 
I'm personally using Ansible and SaltStack.

Ansible is agentless. This being agentless can be a plus option or can be the worst nightmare! 
I would write a blog post someday to describing why!
If you are operating small business or project and your services are less than 5, 15 or even 30 
then everything is normal and you can manually write your inventory file and it is probably the best 
solution because in such cases you with the high change, operating services on the outsourced 
machines.

At some point, many factors will push you to decide to rely on cloud-based 
infrastructures like AWS, Azure, and others, or like my case have to operate your servers in semi-old fashion.

### Ansible
Ansible is one of the leading configuration management tools, written in Python. highly customizable, extendable,
modular and extensively reliable when you want to manage your machines without even single human login!
For whom want my advise: if you are working individually, then it is ok to run Ansible Playbooks and adhoc
from your own workstation, but if you are part of a team, please create a controller machine and always use it
for executing your playbooks! Controller machine will let you manage version of Ansible itself and dependencies
related to your playbook.

### OpenNebula
OpenNebula is one of the popular choices amongst virtualization softwares. OpenNebula
introduce itself in this correct way:

> If you were looking for an open source, enterprise-ready solution to build your Elastic Private Cloud, 
> well, you just found it! Combine VMWare vCenter and KVM virtual machines for fully virtualized clouds, 
> LXD system containers for containerized clouds, and Firecracker micro-VMs for serverless deployments. 
> Integrate them with cloud providers like AWS, Azure and Packet and create flexible hybrid and edge cloud 
> infrastructures.

Do you remember when I told you it is ok if you can manage your inventory manually, 
well it becomes impossible when you using virtualizing solutions. You would
become crazy when machines increasing in number (think about 500, 700 even 1500 and more)
which creating and removing many times every day! well, if you want to still manage your inventory manually, 
be worry that if one IP reassign to a new machine.
If you don't update your repository and push it exactly after this change, there is a chance that one of your
teammates run a playbook on host groups that this IP was part of it.

## Required Libraries
* PyOne
* YAML

YAML related libraries already are in your default installed packages, but you can install pyone with below command:
```bash
python -m pip install pyone
```

## Setup
Copy `opennebula_inventory.py` into Ansible's predefined module's path.

## Examples
```yaml
- name: create yaml formatted inventory file from opennebula hosted virtual machines
  opennebula-inventory:
    api: "https://domain.tld:2633/RPC2"
    username: opennebula-username
    password: opennebula-password
    dest: /tmp/inventory.yaml
```
