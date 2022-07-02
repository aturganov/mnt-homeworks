# Домашнее задание к занятию "08.03 Использование Yandex Cloud"

## Подготовка к выполнению

1. Подготовьте в Yandex Cloud три хоста: для `clickhouse`, для `vector` и для `lighthouse`.
```
Подготовлены машины:
[locadm@vds2295339 ~]$ yc compute instance list 
+----------------------+---------------+---------------+---------+---------------+-------------+
|          ID          |     NAME      |    ZONE ID    | STATUS  |  EXTERNAL IP  | INTERNAL IP |
+----------------------+---------------+---------------+---------+---------------+-------------+
| epd89gf0t5k94q1nvqr8 | lighthouse-01 | ru-central1-b | RUNNING | 51.250.29.247 | 10.1.2.23   |
| epd9no1el2vterouvngm | clickhouse-01 | ru-central1-b | RUNNING | 62.84.121.143 | 10.1.2.9    |
| epdkvk6skl0su9p2u80u | vector-01     | ru-central1-b | RUNNING | 51.250.23.134 | 10.1.2.6    |
```
## Основная часть

1. Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает lighthouse.
```
В проекте: 
https://github.com/aturganov/work_mnt_playbook/tree/8.3
```
2. При создании tasks рекомендую использовать модули: `get_url`, `template`, `yum`, `apt`.
3. Tasks должны: скачать статику lighthouse, установить nginx или любой другой webserver, настроить его конфиг для открытия lighthouse, запустить webserver.
4. Приготовьте свой собственный inventory файл `prod.yml`.
5. Запустите `ansible-lint site.yml` и исправьте ошибки, если они есть.
6. Попробуйте запустить playbook на этом окружении с флагом `--check`.
7. Запустите playbook на `prod.yml` окружении с флагом `--diff`. Убедитесь, что изменения на системе произведены.
8. Повторно запустите playbook с флагом `--diff` и убедитесь, что playbook идемпотентен.
9. Подготовьте README.md файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
```

```
10. Готовый playbook выложите в свой репозиторий, поставьте тег `08-ansible-03-yandex` на фиксирующий коммит, в ответ предоставьте ссылку на него.
---
```
[locadm@vds2295339 playbook]$ ansible-playbook -i inventory/prod.yml site.yml

PLAY [Install NGINX] ******************************************************************************

TASK [Gathering Facts] ****************************************************************************
ok: [lighthouse-01]

TASK [NGINX | Install release] ********************************************************************
ok: [lighthouse-01]

TASK [NGINX | Install NGINX] **********************************************************************
ok: [lighthouse-01]

TASK [NGINX | Create general config] **************************************************************
ok: [lighthouse-01]

PLAY [Install lighthouse] *************************************************************************

TASK [Gathering Facts] ****************************************************************************
ok: [lighthouse-01]

TASK [lighthouse | install dependencies] **********************************************************
ok: [lighthouse-01]

TASK [lighthouse | copy from git] *****************************************************************
ok: [lighthouse-01]

TASK [lighthouse | create lighthouse config] ******************************************************
ok: [lighthouse-01]

PLAY [Install Clickhouse] *************************************************************************

TASK [Gathering Facts] ****************************************************************************
ok: [clickhouse-01]

TASK [Get clickhouse distrib] *********************************************************************
ok: [clickhouse-01] => (item=clickhouse-client)
ok: [clickhouse-01] => (item=clickhouse-server)
failed: [clickhouse-01] (item=clickhouse-common-static) => {"ansible_loop_var": "item", "changed": false, "dest": "./clickhouse-common-static-22.3.3.44.rpm", "elapsed": 0, "gid": 1000, "group": "locadm", "item": "clickhouse-common-static", "mode": "0664", "msg": "Request failed", "owner": "locadm", "response": "HTTP Error 404: Not Found", "secontext": "unconfined_u:object_r:user_home_t:s0", "size": 246310036, "state": "file", "status_code": 404, "uid": 1000, "url": "https://packages.clickhouse.com/rpm/stable/clickhouse-common-static-22.3.3.44.noarch.rpm"}

TASK [Get clickhouse distrib] *********************************************************************
ok: [clickhouse-01]

TASK [Install clickhouse packages] ****************************************************************
ok: [clickhouse-01]

TASK [Create database] ****************************************************************************
ok: [clickhouse-01]

PLAY [Install vector] *****************************************************************************

TASK [Gathering Facts] ****************************************************************************
ok: [vector-01]

TASK [Get vector distrib] *************************************************************************
ok: [vector-01] => (item=vector)

TASK [Install vector package] *********************************************************************
ok: [vector-01]

TASK [Vector | Template config] *******************************************************************
[WARNING]: The value 1000 (type int) in a string field was converted to u'1000' (type string). If
this does not look like what you expect, quote the entire value to ensure it does not change.
ok: [vector-01]

TASK [vector | create unit] ***********************************************************************
ok: [vector-01]

TASK [vector | start sevice] **********************************************************************
fatal: [vector-01]: FAILED! => {"changed": false, "msg": "Unsupported parameters for (ansible.builtin.systemd) module: become Supported parameters include: daemon_reexec, daemon_reload, enabled, force, masked, name, no_block, scope, state, user"}

PLAY RECAP ****************************************************************************************
clickhouse-01              : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0   
lighthouse-01              : ok=8    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
vector-01                  : ok=5    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   

[locadm@vds2295339 playbook]$ ansible-playbook -i inventory/prod.yml site.yml

PLAY [Install NGINX] ******************************************************************************

TASK [Gathering Facts] ****************************************************************************
ok: [lighthouse-01]

TASK [NGINX | Install release] ********************************************************************
ok: [lighthouse-01]

TASK [NGINX | Install NGINX] **********************************************************************
ok: [lighthouse-01]

TASK [NGINX | Create general config] **************************************************************
ok: [lighthouse-01]

PLAY [Install lighthouse] *************************************************************************

TASK [Gathering Facts] ****************************************************************************
ok: [lighthouse-01]

TASK [lighthouse | install dependencies] **********************************************************
ok: [lighthouse-01]

TASK [lighthouse | copy from git] *****************************************************************
ok: [lighthouse-01]

TASK [lighthouse | create lighthouse config] ******************************************************
ok: [lighthouse-01]

PLAY [Install Clickhouse] *************************************************************************

TASK [Gathering Facts] ****************************************************************************
ok: [clickhouse-01]

TASK [Get clickhouse distrib] *********************************************************************
ok: [clickhouse-01] => (item=clickhouse-client)
ok: [clickhouse-01] => (item=clickhouse-server)
failed: [clickhouse-01] (item=clickhouse-common-static) => {"ansible_loop_var": "item", "changed": false, "dest": "./clickhouse-common-static-22.3.3.44.rpm", "elapsed": 0, "gid": 1000, "group": "locadm", "item": "clickhouse-common-static", "mode": "0664", "msg": "Request failed", "owner": "locadm", "response": "HTTP Error 404: Not Found", "secontext": "unconfined_u:object_r:user_home_t:s0", "size": 246310036, "state": "file", "status_code": 404, "uid": 1000, "url": "https://packages.clickhouse.com/rpm/stable/clickhouse-common-static-22.3.3.44.noarch.rpm"}

TASK [Get clickhouse distrib] *********************************************************************
ok: [clickhouse-01]

TASK [Install clickhouse packages] ****************************************************************
ok: [clickhouse-01]

TASK [Create database] ****************************************************************************
ok: [clickhouse-01]

PLAY [Install vector] *****************************************************************************

TASK [Gathering Facts] ****************************************************************************
ok: [vector-01]

TASK [Get vector distrib] *************************************************************************
ok: [vector-01] => (item=vector)

TASK [Install vector package] *********************************************************************
ok: [vector-01]

TASK [Vector | Template config] *******************************************************************
[WARNING]: The value 1000 (type int) in a string field was converted to u'1000' (type string). If
this does not look like what you expect, quote the entire value to ensure it does not change.
ok: [vector-01]

TASK [vector | create unit] ***********************************************************************
ok: [vector-01]

TASK [vector | start sevice] **********************************************************************
ok: [vector-01]

PLAY RECAP ****************************************************************************************
clickhouse-01              : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0   
lighthouse-01              : ok=8    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
vector-01                  : ok=6    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
