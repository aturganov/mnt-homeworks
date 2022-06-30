# Домашнее задание к занятию "08.02 Работа с Playbook"

## Подготовка к выполнению

1. Создайте свой собственный (или используйте старый) публичный репозиторий на github с произвольным именем.
```
https://github.com/aturganov/work_mnt_playbook
```
2. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.
```
https://github.com/aturganov/work_mnt_playbook/tree/master/playbook
```
3. Подготовьте хосты в соответствии с группами из предподготовленного playbook.
```
Установка будет производится на localhost
```

## Основная часть

1. Приготовьте свой собственный inventory файл `prod.yml`.
```
---
clickhouse:
  hosts:
    clickhouse-01:
      ansible_host: localhost
vector:
  hosts:
    vector-01:
      ansible_host: localhost
```
2. Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает [vector](https://vector.dev).
```
[locadm@vds2295339 playbook]$ ansible-playbook site.yml -i inventory/prod.yml -kK -vv
ansible-playbook 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/locadm/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible-playbook
  python version = 2.7.5 (default, Nov 16 2020, 22:23:17) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
Using /etc/ansible/ansible.cfg as config file
SSH password: 
BECOME password[defaults to SSH password]: 
Skipping callback 'actionable', as we already have a stdout callback.
Skipping callback 'counter_enabled', as we already have a stdout callback.
Skipping callback 'debug', as we already have a stdout callback.
Skipping callback 'dense', as we already have a stdout callback.
Skipping callback 'dense', as we already have a stdout callback.
Skipping callback 'full_skip', as we already have a stdout callback.
Skipping callback 'json', as we already have a stdout callback.
Skipping callback 'minimal', as we already have a stdout callback.
Skipping callback 'null', as we already have a stdout callback.
Skipping callback 'oneline', as we already have a stdout callback.
Skipping callback 'selective', as we already have a stdout callback.
Skipping callback 'skippy', as we already have a stdout callback.
Skipping callback 'stderr', as we already have a stdout callback.
Skipping callback 'unixy', as we already have a stdout callback.
Skipping callback 'yaml', as we already have a stdout callback.

PLAYBOOK: site.yml *******************************************************************************************************************************************
1 plays in site.yml

PLAY [Install vector] ****************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************
task path: /home/locadm/git/work_mnt_playbook/playbook/site.yml:36
ok: [vector-01]
META: ran handlers

TASK [Get vector distrib] ************************************************************************************************************************************
task path: /home/locadm/git/work_mnt_playbook/playbook/site.yml:46
ok: [vector-01] => (item=vector) => {"ansible_loop_var": "item", "changed": false, "dest": "./vector-0.22.3.rpm", "elapsed": 16, "gid": 1000, "group": "locadm", "item": "vector", "mode": "0664", "msg": "HTTP Error 304: Not Modified", "owner": "locadm", "size": 62584304, "state": "file", "uid": 1000, "url": "https://packages.timber.io/vector/0.22.3/vector-0.22.3-1.x86_64.rpm"}

TASK [Install vector package] ********************************************************************************************************************************
task path: /home/locadm/git/work_mnt_playbook/playbook/site.yml:52
ok: [vector-01] => {"changed": false, "msg": "", "rc": 0, "results": ["vector-0.22.3-1.x86_64 providing vector-0.22.3.rpm is already installed"]}
META: ran handlers
META: ran handlers

PLAY RECAP ***************************************************************************************************************************************************
vector-01                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[locadm@vds2295339 playbook]$ ansible-playbook site.yml -i inventory/prod.yml -kK -v
Using /etc/ansible/ansible.cfg as config file
SSH password: 
BECOME password[defaults to SSH password]: 

PLAY [Install vector] ****************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************
ok: [vector-01]

TASK [Get vector distrib] ************************************************************************************************************************************
ok: [vector-01] => (item=vector) => {"ansible_loop_var": "item", "changed": false, "dest": "./vector-0.22.3.rpm", "elapsed": 9, "gid": 1000, "group": "locadm", "item": "vector", "mode": "0664", "msg": "HTTP Error 304: Not Modified", "owner": "locadm", "size": 62584304, "state": "file", "uid": 1000, "url": "https://packages.timber.io/vector/0.22.3/vector-0.22.3-1.x86_64.rpm"}

TASK [Install vector package] ********************************************************************************************************************************
ok: [vector-01] => {"changed": false, "msg": "", "rc": 0, "results": ["vector-0.22.3-1.x86_64 providing vector-0.22.3.rpm is already installed"]}

PLAY RECAP ***************************************************************************************************************************************************
vector-01                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```
3. При создании tasks рекомендую использовать модули: `get_url`, `template`, `unarchive`, `file`.
```
выше лог
```
4. Tasks должны: скачать нужной версии дистрибутив, выполнить распаковку в выбранную директорию, установить vector.
```
выше лог
```
5. Запустите `ansible-lint site.yml` и исправьте ошибки, если они есть.
```
[locadm@vds2295339 playbook]$ ansible-lint site.yml
[locadm@vds2295339 playbook]$ 

Ошибок нет
```
6. Попробуйте запустить playbook на этом окружении с флагом `--check`.
```
[locadm@vds2295339 playbook]$ ansible-playbook site.yml -i inventory/prod.yml -kK -v --check
Using /etc/ansible/ansible.cfg as config file
SSH password: 
BECOME password[defaults to SSH password]: 

PLAY [Install vector] ****************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************
ok: [vector-01]

TASK [Get vector distrib] ************************************************************************************************************************************
ok: [vector-01] => (item=vector) => {"ansible_loop_var": "item", "changed": false, "dest": "./vector-0.22.3.rpm", "elapsed": 16, "gid": 1000, "group": "locadm", "item": "vector", "mode": "0664", "msg": "HTTP Error 304: Not Modified", "owner": "locadm", "size": 62584304, "state": "file", "uid": 1000, "url": "https://packages.timber.io/vector/0.22.3/vector-0.22.3-1.x86_64.rpm"}

TASK [Install vector package] ********************************************************************************************************************************
ok: [vector-01] => {"changed": false, "msg": "", "rc": 0, "results": ["vector-0.22.3-1.x86_64 providing vector-0.22.3.rpm is already installed"]}

PLAY RECAP ***************************************************************************************************************************************************
vector-01                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
7. Запустите playbook на `prod.yml` окружении с флагом `--diff`. Убедитесь, что изменения на системе произведены.
```
[locadm@vds2295339 playbook]$ ansible-playbook site.yml -i inventory/prod.yml -kK -v --diff
Using /etc/ansible/ansible.cfg as config file
SSH password: 
BECOME password[defaults to SSH password]: 

PLAY [Install vector] ****************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************
ok: [vector-01]

TASK [Get vector distrib] ************************************************************************************************************************************
ok: [vector-01] => (item=vector) => {"ansible_loop_var": "item", "changed": false, "dest": "./vector-0.22.3.rpm", "elapsed": 9, "gid": 1000, "group": "locadm", "item": "vector", "mode": "0664", "msg": "HTTP Error 304: Not Modified", "owner": "locadm", "size": 62584304, "state": "file", "uid": 1000, "url": "https://packages.timber.io/vector/0.22.3/vector-0.22.3-1.x86_64.rpm"}

TASK [Install vector package] ********************************************************************************************************************************
ok: [vector-01] => {"changed": false, "msg": "", "rc": 0, "results": ["vector-0.22.3-1.x86_64 providing vector-0.22.3.rpm is already installed"]}

PLAY RECAP ***************************************************************************************************************************************************
vector-01                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
8. Повторно запустите playbook с флагом `--diff` и убедитесь, что playbook идемпотентен.
```
[locadm@vds2295339 playbook]$ ansible-playbook site.yml -i inventory/prod.yml -kK -v --diff
Using /etc/ansible/ansible.cfg as config file
SSH password: 
BECOME password[defaults to SSH password]: 

PLAY [Install vector] ****************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************
ok: [vector-01]

TASK [Get vector distrib] ************************************************************************************************************************************
ok: [vector-01] => (item=vector) => {"ansible_loop_var": "item", "changed": false, "dest": "./vector-0.22.3.rpm", "elapsed": 9, "gid": 1000, "group": "locadm", "item": "vector", "mode": "0664", "msg": "HTTP Error 304: Not Modified", "owner": "locadm", "size": 62584304, "state": "file", "uid": 1000, "url": "https://packages.timber.io/vector/0.22.3/vector-0.22.3-1.x86_64.rpm"}

TASK [Install vector package] ********************************************************************************************************************************
ok: [vector-01] => {"changed": false, "msg": "", "rc": 0, "results": ["vector-0.22.3-1.x86_64 providing vector-0.22.3.rpm is already installed"]}

PLAY RECAP ***************************************************************************************************************************************************
vector-01                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
9. Подготовьте README.md файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
```
Сценарций playbook:
1) Настройка хоста - localhost c подключением через пользователя (текущего) locadm с привелегией sudo. Ввод  (Параметры -kK при запуске ansible-play). Вход через ssh по паролю на пользоваетеля locadm.
2) Скачивание дистрибутива vector и сохранение в локальной папке.
3) Установка приложения.
```

10. Готовый playbook выложите в свой репозиторий, поставьте тег `08-ansible-02-playbook` на фиксирующий коммит, в ответ предоставьте ссылку на него.
```
https://github.com/aturganov/work_mnt_playbook/tree/08-ansible-02-playbook
```
---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
