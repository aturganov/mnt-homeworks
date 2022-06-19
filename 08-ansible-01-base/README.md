# Домашнее задание к занятию "08.01 Введение в Ansible"

## Подготовка к выполнению
1. Установите ansible версии 2.10 или выше.
```gitignore
python3 -m pip install --user ansible
```   
2. Создайте свой собственный публичный репозиторий на github с произвольным именем.
```gitignore
https://github.com/aturganov/ansible_task
```
3. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.
```gitignore
Скачал
```
## Основная часть
1. Попробуйте запустить playbook на окружении из `test.yml`, зафиксируйте какое значение имеет факт `some_fact` для указанного хоста при выполнении playbook'a.
```gitignore
turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-playbook site.yml -i inventory/test.yml

PLAY [Print os facts] *********************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************
ok: [localhost]

TASK [Print OS] ***************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] *************************************************************************************************************************************************
ok: [localhost] => {
    "msg": 12
}

PLAY RECAP ********************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

Значение some_fact берется из файла переменных ниже:
```
![img.png](img.png)
2. Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.
```gitignore
Внес изменения
turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-playbook site.yml -i inventory/test.yml

PLAY [Print os facts] *********************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************
ok: [localhost]

TASK [Print OS] ***************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] *************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "all default fact"
}

PLAY RECAP ********************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
3. Воспользуйтесь подготовленным (используется `docker`) или создайте собственное окружение для проведения дальнейших испытаний.
   
```gitignore
turganovai@vds2260027:~/git/ansible_task/playbook$ docker version
Client: Docker Engine - Community
 Version:           20.10.15
 API version:       1.41
 Go version:        go1.17.9
Накидал контейнеров:


1.Dokerfile

FROM ubuntu:latest

LABEL label="ubuntu"

RUN apt-get -y update
RUN apt-get -y install nginx

RUN apt-get -y install python3
# RUN apt-get -y install python

ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]

docker_compose.1.yml

version: '3.5'
services:
  centos7:
    build:
      context: .
      dockerfile: 1.dockerfile
    container_name: centos7

2.Dockerfile
FROM centos:7


LABEL label="centos7"

RUN yum -y install epel-release
RUN yum -y update
RUN yum -y install nginx

ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]

docker_compose.2.yml
version: '3.5'
services:
  centos7:
    build:
      context: .
      dockerfile: 2.dockerfile
    container_name: centos7


```
4. Проведите запуск playbook на окружении из `prod.yml`. Зафиксируйте полученные значения `some_fact` для каждого из `managed host`.
```gitignore
    turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-playbook -i inventory/prod.yml site.yml 

PLAY [Print os facts] ***********************************************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] *****************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ***************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el"
}
ok: [ubuntu] => {
    "msg": "deb"
}

PLAY RECAP **********************************************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
5. Добавьте факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились следующие значения: для `deb` - 'deb default fact', для `el` - 'el default fact'.
```gitignore
cat /group_vars/deb/examp.yml
---
  # some_fact: "deb"
  some_fact: "deb default fact"
  
cat /group_vars/el/examp.yml
---
  # some_fact: "el"
  some_fact: "el default fact"
```
6.  Повторите запуск playbook на окружении `prod.yml`. Убедитесь, что выдаются корректные значения для всех хостов.
```gitignore
turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-playbook -i inventory/prod.yml site.yml 

PLAY [Print os facts] ********************************************************************************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **************************************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ************************************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP *******************************************************************************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

turganovai@vds2260027:~/git/ansible_task/playbook$ 
```
7. При помощи `ansible-vault` зашифруйте факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.
```gitignore
turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-vault encrypt group_vars/deb/examp.yml
New Vault password: 
Confirm New Vault password: 
Encryption successful

turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-vault encrypt group_vars/el/examp.yml 
New Vault password: 
Confirm New Vault password: 
Encryption successful
```
8. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь в работоспособности.
```gitignore
turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-playbook -i inventory/prod.yml site.yml --ask-vault-pass
Vault password: 

PLAY [Print os facts] *********************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ***************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] *************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP ********************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
9. Посмотрите при помощи `ansible-doc` список плагинов для подключения. Выберите подходящий для работы на `control node`.
```gitignore
Думаю local

turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-doc -t connection -l
[WARNING]: Collection splunk.es does not support Ansible version 2.12.5
[WARNING]: Collection ibm.qradar does not support Ansible version 2.12.5
[WARNING]: Collection frr.frr does not support Ansible version 2.12.5
[DEPRECATION WARNING]: ansible.netcommon.napalm has been deprecated. See the plugin documentation for more details. This feature will be removed from ansible.netcommon in a release after 
2022-06-01. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ansible.netcommon.httpapi      Use httpapi to run command on network appliances                                                                                                            
ansible.netcommon.libssh       (Tech preview) Run tasks using libssh for ssh connection                                                                                                    
ansible.netcommon.napalm       Provides persistent connection using NAPALM                                                                                                                 
ansible.netcommon.netconf      Provides a persistent connection using the netconf protocol                                                                                                 
ansible.netcommon.network_cli  Use network_cli to run command on network appliances                                                                                                        
ansible.netcommon.persistent   Use a persistent unix socket for connection                                                                                                                 
community.aws.aws_ssm          execute via AWS Systems Manager                                                                                                                             
community.docker.docker        Run tasks in docker containers                                                                                                                              
community.docker.docker_api    Run tasks in docker containers                                                                                                                              
community.docker.nsenter       execute on host running controller container                                                                                                                
community.general.chroot       Interact with local chroot                                                                                                                                  
community.general.funcd        Use funcd to connect to target                                                                                                                              
community.general.iocage       Run tasks in iocage jails                                                                                                                                   
community.general.jail         Run tasks in jails                                                                                                                                          
community.general.lxc          Run tasks in lxc containers via lxc python library                                                                                                          
community.general.lxd          Run tasks in lxc containers via lxc CLI                                                                                                                     
community.general.qubes        Interact with an existing QubesOS AppVM                                                                                                                     
community.general.saltstack    Allow ansible to piggyback on salt minions                                                                                                                  
community.general.zone         Run tasks in a zone instance                                                                                                                                
community.libvirt.libvirt_lxc  Run tasks in lxc containers via libvirt                                                                                                                     
community.libvirt.libvirt_qemu Run tasks on libvirt/qemu virtual machines                                                                                                                  
community.okd.oc               Execute tasks in pods running on OpenShift                                                                                                                  
community.vmware.vmware_tools  Execute tasks inside a VM via VMware Tools                                                                                                                  
community.zabbix.httpapi       Use httpapi to run command on network appliances                                                                                                            
containers.podman.buildah      Interact with an existing buildah container                                                                                                                 
containers.podman.podman       Interact with an existing podman container                                                                                                                  
kubernetes.core.kubectl        Execute tasks in pods running on Kubernetes                                                                                                                 
local                          execute on controller                                                                                                                                       
paramiko_ssh                   Run tasks via python ssh (paramiko)                                                                                                                         
psrp                           Run tasks over Microsoft PowerShell Remoting Protocol                                                                                                       
ssh                            connect via SSH client binary                                                                                                                               
winrm                          Run tasks over Microsoft's WinRM                  
```
10. В `prod.yml` добавьте новую группу хостов с именем  `local`, в ней разместите localhost с необходимым типом подключения.
```gitignore
---
  el:
    hosts:
      centos7:
        ansible_connection: docker
  deb:
    hosts:
      ubuntu:
        ansible_connection: docker
  local:
    hosts:
      localhost:
        ansible_connection: local
        
turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-playbook -i inventory/prod.yml site.yml --ask-vault-pass
Vault password: 

PLAY [Print os facts] **************************************************************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************************************************************
ok: [localhost]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ********************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [localhost] => {
    "msg": "Ubuntu"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
ok: [localhost] => {
    "msg": "all default fact"
}

PLAY RECAP *************************************************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

11. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь что факты `some_fact` для каждого из хостов определены из верных `group_vars`.
```gitignore
добавил group_vars 
local
---
  some_fact: "local default fact"


turganovai@vds2260027:~/git/ansible_task/playbook$ ansible-playbook -i inventory/prod.yml site.yml --ask-vault-pass
Vault password: 

PLAY [Print os facts] **************************************************************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************************************************************
ok: [localhost]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ********************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ******************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
ok: [localhost] => {
    "msg": "local default fact"
}

PLAY RECAP *************************************************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```
12. Заполните `README.md` ответами на вопросы. Сделайте `git push` в ветку `master`. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым `playbook` и заполненным `README.md`.

## Необязательная часть

1. При помощи `ansible-vault` расшифруйте все зашифрованные файлы с переменными.
2. Зашифруйте отдельное значение `PaSSw0rd` для переменной `some_fact` паролем `netology`. Добавьте полученное значение в `group_vars/all/exmp.yml`.
3. Запустите `playbook`, убедитесь, что для нужных хостов применился новый `fact`.
4. Добавьте новую группу хостов `fedora`, самостоятельно придумайте для неё переменную. В качестве образа можно использовать [этот](https://hub.docker.com/r/pycontribs/fedora).
5. Напишите скрипт на bash: автоматизируйте поднятие необходимых контейнеров, запуск ansible-playbook и остановку контейнеров.
6. Все изменения должны быть зафиксированы и отправлены в вашей личный репозиторий.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
