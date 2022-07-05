# Домашнее задание к занятию "8.4 Работа с Roles"

## Подготовка к выполнению
1. Создайте два пустых публичных репозитория в любом своём проекте: vector-role и lighthouse-role.


2. Добавьте публичную часть своего ключа к своему профилю в github.

## Основная часть

Наша основная цель - разбить наш playbook на отдельные roles. Задача: сделать roles для clickhouse, vector и lighthouse и написать playbook для использования этих ролей. Ожидаемый результат: существуют три ваших репозитория: два с roles и один с playbook.

1. Создать в старой версии playbook файл `requirements.yml` и заполнить его следующим содержимым:

   ```yaml
   ---
     - src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
       scm: git
       version: "1.11.0"
       name: clickhouse 
   ```

2. При помощи `ansible-galaxy` скачать себе эту роль.
3. Создать новый каталог с ролью при помощи `ansible-galaxy role init vector-role`.
4. На основе tasks из старого playbook заполните новую role. Разнесите переменные между `vars` и `default`. 
5. Перенести нужные шаблоны конфигов в `templates`.
6. Описать в `README.md` обе роли и их параметры.
7. Повторите шаги 3-6 для lighthouse. Помните, что одна роль должна настраивать один продукт.
8. Выложите все roles в репозитории. Проставьте тэги, используя семантическую нумерацию Добавьте roles в `requirements.yml` в playbook.
9. Переработайте playbook на использование roles. Не забудьте про зависимости lighthouse и возможности совмещения `roles` с `tasks`.
10. Выложите playbook в репозиторий.
11. В ответ приведите ссылки на оба репозитория с roles и одну ссылку на репозиторий с playbook.
```
https://github.com/aturganov/vector-role
https://github.com/aturganov/lighthouse-role
https://github.com/aturganov/work_mnt_playbook/tree/8.4

```


---
```
Финальный лог
[locadm@vds2295339 work_mnt_playbook]$ ansible-playbook -i inventory/hosts.yml site.yml

PLAY [Add vector role] **********************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************
ok: [vector-01]

TASK [vector-role : Get vector distrib] *****************************************************************************************************************
ok: [vector-01] => (item=vector)

TASK [vector-role : Install vector package] *************************************************************************************************************
ok: [vector-01]

TASK [vector-role : Vector | Template config] ***********************************************************************************************************
[WARNING]: The value 1000 (type int) in a string field was converted to u'1000' (type string). If this does not look like what you expect, quote the
entire value to ensure it does not change.
ok: [vector-01]

TASK [vector-role : vector | create unit] ***************************************************************************************************************
ok: [vector-01]

TASK [vector-role : vector | start sevice] **************************************************************************************************************
ok: [vector-01]

PLAY [Install NGINX & Lighthouse] ***********************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************
ok: [lighthouse-01]

TASK [lighthouse-role : NGINX | Install release] ********************************************************************************************************
ok: [lighthouse-01]

TASK [lighthouse-role : NGINX | Install NGINX] **********************************************************************************************************
ok: [lighthouse-01]

TASK [lighthouse-role : NGINX | Create general config] **************************************************************************************************
ok: [lighthouse-01]

TASK [lighthouse-role : lighthouse | install dependencies] **********************************************************************************************
ok: [lighthouse-01]

TASK [lighthouse-role : lighthouse | copy from git] *****************************************************************************************************
ok: [lighthouse-01]

TASK [lighthouse-role : lighthouse | create lighthouse config] ******************************************************************************************
ok: [lighthouse-01]

PLAY [Install Clickhouse] *******************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : Include OS Family Specific Variables] ****************************************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************
included: /home/locadm/git/work_mnt_playbook/roles/ansible-clickhouse/tasks/precheck.yml for clickhouse-01

TASK [ansible-clickhouse : Requirements check | Checking sse4_2 support] ********************************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : Requirements check | Not supported distribution && release] ******************************************************************
skipping: [clickhouse-01]

TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************
included: /home/locadm/git/work_mnt_playbook/roles/ansible-clickhouse/tasks/params.yml for clickhouse-01

TASK [ansible-clickhouse : Set clickhouse_service_enable] ***********************************************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : Set clickhouse_service_ensure] ***********************************************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************
included: /home/locadm/git/work_mnt_playbook/roles/ansible-clickhouse/tasks/install/yum.yml for clickhouse-01

TASK [ansible-clickhouse : Install by YUM | Ensure clickhouse repo GPG key imported] ********************************************************************
changed: [clickhouse-01]

TASK [ansible-clickhouse : Install by YUM | Ensure clickhouse repo installed] ***************************************************************************
changed: [clickhouse-01]

TASK [ansible-clickhouse : Install by YUM | Ensure clickhouse package installed (latest)] ***************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : Install by YUM | Ensure clickhouse package installed (version latest)] *******************************************************
skipping: [clickhouse-01]

TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************
included: /home/locadm/git/work_mnt_playbook/roles/ansible-clickhouse/tasks/configure/sys.yml for clickhouse-01

TASK [ansible-clickhouse : Check clickhouse config, data and logs] **************************************************************************************
ok: [clickhouse-01] => (item=/var/log/clickhouse-server)
changed: [clickhouse-01] => (item=/etc/clickhouse-server)
changed: [clickhouse-01] => (item=/var/lib/clickhouse/tmp/)
changed: [clickhouse-01] => (item=/var/lib/clickhouse/)

TASK [ansible-clickhouse : Config | Create config.d folder] *********************************************************************************************
changed: [clickhouse-01]

TASK [ansible-clickhouse : Config | Create users.d folder] **********************************************************************************************
changed: [clickhouse-01]

TASK [ansible-clickhouse : Config | Generate system config] *********************************************************************************************
changed: [clickhouse-01]

TASK [ansible-clickhouse : Config | Generate users config] **********************************************************************************************
changed: [clickhouse-01]

TASK [ansible-clickhouse : Config | Generate remote_servers config] *************************************************************************************
skipping: [clickhouse-01]

TASK [ansible-clickhouse : Config | Generate macros config] *********************************************************************************************
skipping: [clickhouse-01]

TASK [ansible-clickhouse : Config | Generate zookeeper servers config] **********************************************************************************
skipping: [clickhouse-01]

TASK [ansible-clickhouse : Config | Fix interserver_http_port and intersever_https_port collision] ******************************************************
skipping: [clickhouse-01]

RUNNING HANDLER [ansible-clickhouse : Restart Clickhouse Service] ***************************************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************
included: /home/locadm/git/work_mnt_playbook/roles/ansible-clickhouse/tasks/service.yml for clickhouse-01

TASK [ansible-clickhouse : Ensure clickhouse-server.service is enabled: True and state: restarted] ******************************************************
changed: [clickhouse-01]

TASK [ansible-clickhouse : Wait for Clickhouse Server to Become Ready] **********************************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************
included: /home/locadm/git/work_mnt_playbook/roles/ansible-clickhouse/tasks/configure/db.yml for clickhouse-01

TASK [ansible-clickhouse : Set ClickHose Connection String] *********************************************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : Gather list of existing databases] *******************************************************************************************
ok: [clickhouse-01]

TASK [ansible-clickhouse : Config | Delete database config] *********************************************************************************************

TASK [ansible-clickhouse : Config | Create database config] *********************************************************************************************

TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************
included: /home/locadm/git/work_mnt_playbook/roles/ansible-clickhouse/tasks/configure/dict.yml for clickhouse-01

TASK [ansible-clickhouse : Config | Generate dictionary config] *****************************************************************************************
skipping: [clickhouse-01]

TASK [ansible-clickhouse : include_tasks] ***************************************************************************************************************
skipping: [clickhouse-01]

PLAY RECAP **********************************************************************************************************************************************
clickhouse-01              : ok=25   changed=8    unreachable=0    failed=0    skipped=10   rescued=0    ignored=0   
lighthouse-01              : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
vector-01                  : ok=6    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
