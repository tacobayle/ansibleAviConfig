# Ansible Avi Configure

## Goals
Configure Avi controller through Ansible for multiple environments (vCenter, NSX-T, AWS, GCP, Azure, OpenStack and VMC).

## Prerequisites:
- The following python packages are installed:
```
sudo apt install -y python3-pip
sudo apt install -y python3-jmespath
pip3 install --upgrade pip
pip3 install ansible-core==2.12.5
pip3 install ansible==5.7.1
pip3 install avisdk
sudo -u ubuntu ansible-galaxy collection install vmware.alb
pip3 install dnspython
pip3 install netaddr
```

- Avi Controller API is reachable (HTTP 443) from your ansible host
- For VMC, make sure the vcenter and ESXi hosts are reachable (HTTP 443) from your ansible host

## Environment:

### OS version:

```
NAME="Ubuntu"
VERSION="20.04.3 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.3 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```

### Ansible version

```
ansible [core 2.12.5]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ubuntu/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.8/dist-packages/ansible
  ansible collection location = /home/ubuntu/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.8.10 (default, Mar 15 2022, 12:22:08) [GCC 9.4.0]
  jinja version = 2.10.1
  libyaml = True
```

### Avi version

```
Avi 21.1.4
avisdk 21.1.4
```

### Avi Environment

- VMware (V-center 6.7.0, ESXi, 6.7.0, 15160138) - with a single controller VM or a cluster of three controller VMs
- AWS
- NSX-T
- GCP
- VMC (No Access)
- OpenStack

## Input/Parameters:

A sample variable file per cloud type is defined in the var directory:
- vars/vcenter.yml

## Use  the ansible playbook to:
- Wait the portal to be active (https port open)
- Bootstrap the controller with a password
- Configure the controller cluster (Vcenter or NSXT environment only)
- Create a backup_passphrase
- Configure system configuration (global, DNS, NTP, email config)
- Configure Cloud, supported clouds are: v-center, was, azure, gcp, openstack, nsxt, no access (for VMC)
- Configure SE group
- Spin-up SE (only for VMC)
- Create a Health Monitor
- Create a Pool (based on the Health Monitor previously created) -  based on servers IP
- Create a Pool (based on the Health Monitor previously created) -  based on NSX-T Group
- Create a Pool (based on the Health Monitor previously created) -  based on AWS ASG
- Create VS(s) based on vs-vip
- Enable a GSLB config (with a local controller and a remote controller)
- Create a GSLB service config

## Run the playbook:
```
git clone https://github.com/tacobayle/ansibleAviConfigure ; ansible-playbook -i hosts aviConfigure/local.yml --extra-vars @vars/fromTerraform.yml
```