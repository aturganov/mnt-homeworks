# Домашнее задание к занятию "08.05 Тестирование Roles"

Исхожу из того, что лектор, к сожалению, нечетко обозначил в задание что нужно. 
Прошу сформулировать при необходимости, что от меня требуется.

Ниже что что сделал.

Репы в репах:
https://github.com/aturganov/work_mnt_playbook/tree/8.5
https://github.com/aturganov/vector-role/tree/8.5

## Подготовка к выполнению
1. Установите molecule: `pip3 install "molecule==3.4.0"`
2. Выполните `docker pull aragast/netology:latest` -  это образ с podman, tox и несколькими пайтонами (3.7 и 3.9) внутри
```
Выполнил
```

## Основная часть

Наша основная цель - настроить тестирование наших ролей. Задача: сделать сценарии тестирования для vector. Ожидаемый результат: все сценарии успешно проходят тестирование ролей.

### Molecule
pip install --upgrade pipe, посмотрите на вывод команды.
2. Перейдите в каталог с ролью vector-role и создайте сценарий тестирования по умолчанию при помощи `molecule init scenario --driver-name docker`.
```
В описании пропущено
pip3 install molecule-docker
Запуск
[locadm@vds2295339 work_mnt_playbook]$ molecule init scenario --driver-name docker
/usr/local/lib/python3.6/site-packages/requests/__init__.py:104: RequestsDependencyWarning: urllib3 (1.26.9) or chardet (5.0.0)/charset_normalizer (2.0.12) doesn't match a supported version!
  RequestsDependencyWarning)
INFO     Initializing new scenario default...
INFO     Initialized scenario in /home/locadm/git/work_mnt_playbook/roles/vector-role/molecule/default successfully.
```
3. Добавьте несколько разных дистрибутивов (centos:8, ubuntu:latest) для инстансов и протестируйте роль, исправьте найденные ошибки, если они есть.
``` 
А что нужно тестировать, работоспособность самой молекулы. Перебрал бесконечное число версий модулей, чтоб он наконец-то заработал. Доустановил модули и пересобрал питон.

Ошибка molecule_docker оказалось для Centos непобедимой. Переписал create.yml, то бишь закоментил ниже указанный блок.
Это косяк многих релизов...

task path: /usr/local/lib/python3.6/site-packages/molecule_docker/playbooks/create.yml:65
fatal: [localhost]: FAILED! => {
    "msg": "The conditional check 'platforms.changed or docker_images.results | map(attribute='images') | select('equalto', []) | list | count >= 0' failed. The error was: no test named 'equalto'\n\nThe error appears to be in '/usr/local/lib/python3.6/site-packages/molecule_docker/playbooks/create.yml': line 65, column 7, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\n    - name: Build an Ansible compatible image (new)  # noqa: no-handler\n      ^ here\n"
}
Молекула наконец то заработала.

[locadm@vds2295339 vector-role]$ molecule test
/usr/local/lib/python3.6/site-packages/requests/__init__.py:104: RequestsDependencyWarning: urllib3 (1.26.9) or chardet (5.0.0)/charset_normalizer (2.0.12) doesn't match a supported version!
  RequestsDependencyWarning)
INFO     default scenario test matrix: dependency, lint, cleanup, destroy, syntax, create, prepare, converge, idempotence, side_effect, verify, cleanup, destroy
INFO     Performing prerun...
INFO     Set ANSIBLE_LIBRARY=/home/locadm/.cache/ansible-compat/151a07/modules:/home/locadm/.ansible/plugins/modules:/usr/share/ansible/plugins/modules
INFO     Set ANSIBLE_COLLECTIONS_PATHS=/home/locadm/.cache/ansible-compat/151a07/collections:/home/locadm/.ansible/collections:/usr/share/ansible/collections
INFO     Set ANSIBLE_ROLES_PATH=/home/locadm/.cache/ansible-compat/151a07/roles:/home/locadm/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles
INFO     Running default > dependency
WARNING  Skipping, missing the requirements file.
WARNING  Skipping, missing the requirements file.
INFO     Running default > lint
INFO     Lint is disabled.
INFO     Running default > cleanup
WARNING  Skipping, cleanup playbook not configured.
INFO     Running default > destroy
INFO     Sanity checks: 'docker'

PLAY [Destroy] *******************************************************************************

TASK [Destroy molecule instance(s)] **********************************************************
changed: [localhost] => (item=instance_centos)

TASK [Wait for instance(s) deletion to complete] *********************************************
changed: [localhost] => (item=instance_centos)

TASK [Delete docker networks(s)] *************************************************************

PLAY RECAP ***********************************************************************************
localhost                  : ok=2    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

INFO     Running default > syntax

playbook: /home/locadm/git/work_mnt_playbook/roles/vector-role/molecule/default/converge.yml
INFO     Running default > create

PLAY [Create] ********************************************************************************

TASK [Log into a Docker registry] ************************************************************
skipping: [localhost] => (item=None) 
skipping: [localhost]

TASK [Check presence of custom Dockerfiles] **************************************************
ok: [localhost] => (item={u'image': u'docker.io/pycontribs/centos:7', u'pre_build_image': True, u'name': u'instance_centos'})

TASK [Create Dockerfiles from image names] ***************************************************
skipping: [localhost] => (item={u'image': u'docker.io/pycontribs/centos:7', u'pre_build_image': True, u'name': u'instance_centos'})

TASK [Discover local Docker images] **********************************************************
ok: [localhost] => (item={u'item': {u'image': u'docker.io/pycontribs/centos:7', u'pre_build_image': True, u'name': u'instance_centos'}, u'skipped': True, u'ansible_loop_var': u'item', u'skip_reason': u'Conditional result was False', u'i': 0, u'ansible_index_var': u'i', u'changed': False})

TASK [Create docker network(s)] **************************************************************

TASK [Determine the CMD directives] **********************************************************
ok: [localhost] => (item={u'image': u'docker.io/pycontribs/centos:7', u'pre_build_image': True, u'name': u'instance_centos'})

TASK [Create molecule instance(s)] ***********************************************************
changed: [localhost] => (item=instance_centos)

TASK [Wait for instance(s) creation to complete] *********************************************
FAILED - RETRYING: Wait for instance(s) creation to complete (300 retries left).
changed: [localhost] => (item={u'ansible_loop_var': u'item', u'ansible_job_id': u'149095423749.17345', u'failed': False, u'started': 1, u'changed': True, u'item': {u'image': u'docker.io/pycontribs/centos:7', u'pre_build_image': True, u'name': u'instance_centos'}, u'finished': 0, u'results_file': u'/home/locadm/.ansible_async/149095423749.17345'})

PLAY RECAP ***********************************************************************************
localhost                  : ok=5    changed=2    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0

INFO     Running default > prepare
WARNING  Skipping, prepare playbook not configured.
INFO     Running default > converge

PLAY [Converge] ******************************************************************************

TASK [Gathering Facts] ***********************************************************************
ok: [instance_centos]

TASK [Include vector-role] *******************************************************************

TASK [vector-role : Get vector distrib] ******************************************************
changed: [instance_centos] => (item=vector)

TASK [vector-role : Install vector package] **************************************************
changed: [instance_centos]

TASK [vector-role : Vector | Template config] ************************************************
[WARNING]: The value 0 (type int) in a string field was converted to u'0' (type string). If
this does not look like what you expect, quote the entire value to ensure it does not change.
changed: [instance_centos]

TASK [vector-role : vector | create unit] ****************************************************
changed: [instance_centos]

TASK [vector-role : vector | start sevice] ***************************************************
fatal: [instance_centos]: FAILED! => {"changed": false, "msg": "failure 1 during daemon-reload: Failed to get D-Bus connection: Operation not permitted\n"}

PLAY RECAP ***********************************************************************************
instance_centos            : ok=5    changed=4    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

CRITICAL Ansible return code was 2, command was: ['ansible-playbook', '--inventory', '/home/locadm/.cache/molecule/vector-role/default/inventory', '--skip-tags', 'molecule-notest,notest', '/home/locadm/git/work_mnt_playbook/roles/vector-role/molecule/default/converge.yml']
WARNING  An error occurred during the test sequence action: 'converge'. Cleaning up.
INFO     Running default > cleanup
WARNING  Skipping, cleanup playbook not configured.
INFO     Running default > destroy

PLAY [Destroy] *******************************************************************************

TASK [Destroy molecule instance(s)] **********************************************************
changed: [localhost] => (item=instance_centos)

TASK [Wait for instance(s) deletion to complete] *********************************************
changed: [localhost] => (item=instance_centos)

TASK [Delete docker networks(s)] *************************************************************

PLAY RECAP ***********************************************************************************
localhost                  : ok=2    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

INFO     Pruning extra files from scenario ephemeral directory

ошибка запуска сервиса в докер связана с тем, что 'по умолчанию' сервисы systemd в докер не получится стартовать
TASK [vector-role : vector | start sevice] ***************************************************
fatal: [instance_centos]: FAILED! => {"changed": false, "msg": "failure 1 during daemon-reload: Failed to get D-Bus connection: Operation not permitted\n"}

Нужно донастраивать "привелегированный запуск в докер". Мне искренне не понятно, что думает команда разработчиков молекулы,
если получается что тест в докере ограничен. Молекулу можно доработать
и включить привелегии (иными словами прокинуть их на базовый линукс). 
https://developers.redhat.com/blog/2014/05/05/running-systemd-within-docker-container

Нашел решение: 
Нужно добавить следущие настройки в task
command: /sbin/init
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    privileged: true
Теперь тест проходит успешно

Данную проблему я обозначил преподавателю и получил ответ, что докер по этой причине в практике они не используют.
И перешли на опенстек.
```
4. Добавьте несколько assert'ов в verify.yml файл для  проверки работоспособности vector-role (проверка, что конфиг валидный, проверка успешности запуска, etc). Запустите тестирование роли повторно и проверьте, что оно прошло успешно.
```
Добавил проверку на наличие файла конфига
[locadm@vds2295339 vector-role]$ molecule test
/usr/local/lib/python3.6/site-packages/requests/__init__.py:104: RequestsDependencyWarning: urllib3 (1.26.9) or chardet (5.0.0)/charset_normalizer (2.0.12) doesn't match a supported version!
  RequestsDependencyWarning)
INFO     default scenario test matrix: dependency, lint, cleanup, destroy, syntax, create, prepare, converge, idempotence, side_effect, verify, cleanup, destroy
INFO     Performing prerun...
INFO     Set ANSIBLE_LIBRARY=/home/locadm/.cache/ansible-compat/151a07/modules:/home/locadm/.ansible/plugins/modules:/usr/share/ansible/plugins/modules
INFO     Set ANSIBLE_COLLECTIONS_PATHS=/home/locadm/.cache/ansible-compat/151a07/collections:/home/locadm/.ansible/collections:/usr/share/ansible/collections
INFO     Set ANSIBLE_ROLES_PATH=/home/locadm/.cache/ansible-compat/151a07/roles:/home/locadm/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles
INFO     Running default > dependency
WARNING  Skipping, missing the requirements file.
WARNING  Skipping, missing the requirements file.
INFO     Running default > lint
INFO     Lint is disabled.
INFO     Running default > cleanup
WARNING  Skipping, cleanup playbook not configured.
INFO     Running default > destroy
INFO     Sanity checks: 'docker'

PLAY [Destroy] **********************************************************************************************************

TASK [Destroy molecule instance(s)] *************************************************************************************
changed: [localhost] => (item=instance_centos)

TASK [Wait for instance(s) deletion to complete] ************************************************************************
ok: [localhost] => (item=instance_centos)

TASK [Delete docker networks(s)] ****************************************************************************************

PLAY RECAP **************************************************************************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

INFO     Running default > syntax

playbook: /home/locadm/git/work_mnt_playbook/roles/vector-role/molecule/default/converge.yml
INFO     Running default > create

PLAY [Create] ***********************************************************************************************************

TASK [Log into a Docker registry] ***************************************************************************************
skipping: [localhost] => (item=None) 
skipping: [localhost]

TASK [Check presence of custom Dockerfiles] *****************************************************************************
ok: [localhost] => (item={u'pre_build_image': True, u'command': u'/sbin/init', u'name': u'instance_centos', u'volumes': [u'/sys/fs/cgroup:/sys/fs/cgroup:ro'], u'image': u'docker.io/pycontribs/centos:7', u'privileged': True})

TASK [Create Dockerfiles from image names] ******************************************************************************
skipping: [localhost] => (item={u'pre_build_image': True, u'command': u'/sbin/init', u'name': u'instance_centos', u'volumes': [u'/sys/fs/cgroup:/sys/fs/cgroup:ro'], u'image': u'docker.io/pycontribs/centos:7', u'privileged': True})

TASK [Discover local Docker images] *************************************************************************************
ok: [localhost] => (item={u'item': {u'pre_build_image': True, u'command': u'/sbin/init', u'name': u'instance_centos', u'volumes': [u'/sys/fs/cgroup:/sys/fs/cgroup:ro'], u'image': u'docker.io/pycontribs/centos:7', u'privileged': True}, u'skipped': True, u'ansible_loop_var': u'item', u'skip_reason': u'Conditional result was False', u'i': 0, u'ansible_index_var': u'i', u'changed': False})

TASK [Create docker network(s)] *****************************************************************************************

TASK [Determine the CMD directives] *************************************************************************************
ok: [localhost] => (item={u'pre_build_image': True, u'command': u'/sbin/init', u'name': u'instance_centos', u'volumes': [u'/sys/fs/cgroup:/sys/fs/cgroup:ro'], u'image': u'docker.io/pycontribs/centos:7', u'privileged': True})

TASK [Create molecule instance(s)] **************************************************************************************
changed: [localhost] => (item=instance_centos)

TASK [Wait for instance(s) creation to complete] ************************************************************************
FAILED - RETRYING: Wait for instance(s) creation to complete (300 retries left).
changed: [localhost] => (item={u'ansible_loop_var': u'item', u'ansible_job_id': u'808227003578.27067', u'failed': False, u'started': 1, u'changed': True, u'item': {u'pre_build_image': True, u'command': u'/sbin/init', u'name': u'instance_centos', u'volumes': [u'/sys/fs/cgroup:/sys/fs/cgroup:ro'], u'image': u'docker.io/pycontribs/centos:7', u'privileged': True}, u'finished': 0, u'results_file': u'/home/locadm/.ansible_async/808227003578.27067'})

PLAY RECAP **************************************************************************************************************
localhost                  : ok=5    changed=2    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0

INFO     Running default > prepare
WARNING  Skipping, prepare playbook not configured.
INFO     Running default > converge

PLAY [Converge] *********************************************************************************************************

TASK [Gathering Facts] **************************************************************************************************
ok: [instance_centos]

TASK [Include vector-role] **********************************************************************************************

TASK [vector-role : Get vector distrib] *********************************************************************************
changed: [instance_centos] => (item=vector)

TASK [vector-role : Install vector package] *****************************************************************************
changed: [instance_centos]

TASK [vector-role : Vector | Template config] ***************************************************************************
[WARNING]: The value 0 (type int) in a string field was converted to u'0' (type string). If this does not look like what
you expect, quote the entire value to ensure it does not change.
changed: [instance_centos]

TASK [vector-role : vector | create unit] *******************************************************************************
changed: [instance_centos]

TASK [vector-role : vector | start sevice] ******************************************************************************
changed: [instance_centos]

PLAY RECAP **************************************************************************************************************
instance_centos            : ok=6    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

INFO     Running default > idempotence

PLAY [Converge] *********************************************************************************************************

TASK [Gathering Facts] **************************************************************************************************
ok: [instance_centos]

TASK [Include vector-role] **********************************************************************************************

TASK [vector-role : Get vector distrib] *********************************************************************************
ok: [instance_centos] => (item=vector)

TASK [vector-role : Install vector package] *****************************************************************************
ok: [instance_centos]

TASK [vector-role : Vector | Template config] ***************************************************************************
[WARNING]: The value 0 (type int) in a string field was converted to u'0' (type string). If this does not look like what
you expect, quote the entire value to ensure it does not change.
ok: [instance_centos]

TASK [vector-role : vector | create unit] *******************************************************************************
ok: [instance_centos]

TASK [vector-role : vector | start sevice] ******************************************************************************
ok: [instance_centos]

PLAY RECAP **************************************************************************************************************
instance_centos            : ok=6    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

INFO     Idempotence completed successfully.
INFO     Running default > side_effect
WARNING  Skipping, side effect playbook not configured.
INFO     Running default > verify
INFO     Running Ansible Verifier

PLAY [Verify] ***********************************************************************************************************

TASK [get path config] **************************************************************************************************
ok: [instance_centos]

TASK [check if /file exists] ********************************************************************************************
ok: [instance_centos] => {
    "changed": false, 
    "msg": "/vector.yml exists"
}

PLAY RECAP **************************************************************************************************************
instance_centos            : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

INFO     Verifier completed successfully.
INFO     Running default > cleanup
WARNING  Skipping, cleanup playbook not configured.
INFO     Running default > destroy

PLAY [Destroy] **********************************************************************************************************

TASK [Destroy molecule instance(s)] *************************************************************************************
changed: [localhost] => (item=instance_centos)

TASK [Wait for instance(s) deletion to complete] ************************************************************************
FAILED - RETRYING: Wait for instance(s) deletion to complete (300 retries left).
changed: [localhost] => (item=instance_centos)

TASK [Delete docker networks(s)] ****************************************************************************************

PLAY RECAP **************************************************************************************************************
localhost                  : ok=2    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
INFO     Pruning extra files from scenario ephemeral directory
```

5. Добавьте новый тег на коммит с рабочим сценарием в соответствии с семантическим версионированием.

### Tox

1. Добавьте в директорию с vector-role файлы из [директории](./example)
2. Запустите `docker run --privileged=True -v <path_to_repo>:/opt/vector-role -w /opt/vector-role -it aragast/netology:latest /bin/bash`, где path_to_repo - путь до корня репозитория с vector-role на вашей файловой системе.
3. Внутри контейнера выполните команду `tox`, посмотрите на вывод.
5. Создайте облегчённый сценарий для `molecule` с драйвером `molecule_podman`. Проверьте его на исполнимость.
6. Пропишите правильную команду в `tox.ini` для того чтобы запускался облегчённый сценарий.
8. Запустите команду `tox`. Убедитесь, что всё отработало успешно.
```
Ожидаю либо повтора лекции с более понятным объяснением это блока, либо более четкого задания. Мне непонятно, 
ЧТО НУЖНО СДЕЛАТЬ!

[root@41a76ef6ae7c vector-role]# tox
py38-ansible210 create: /opt/vector-role/.tox/py38-ansible210
py38-ansible210 installdeps: -rtox-requirements.txt, ansible<3.0
py38-ansible210 installed: ansible==2.10.7,ansible-base==2.10.17,ansible-compat==2.1.0,ansible-lint==5.1.3,arrow==1.2.2,attrs==21.4.0,bcrypt==3.2.2,binaryornot==0.4.4,bracex==2.3.post1,Cerberus==1.3.2,certifi==2022.6.15,cffi==1.15.1,chardet==5.0.0,charset-normalizer==2.1.0,click==8.1.3,click-help-colors==0.9.1,commonmark==0.9.1,cookiecutter==2.1.1,cryptography==37.0.4,distro==1.7.0,docker==5.0.3,enrich==1.2.7,idna==3.3,importlib-resources==5.8.0,Jinja2==3.1.2,jinja2-time==0.2.0,jmespath==1.0.1,jsonschema==4.6.2,lxml==4.9.1,MarkupSafe==2.1.1,molecule==3.4.0,molecule-docker==1.1.0,packaging==21.3,paramiko==2.11.0,pathspec==0.9.0,pluggy==0.13.1,pycparser==2.21,Pygments==2.12.0,PyNaCl==1.5.0,pyparsing==3.0.9,pyrsistent==0.18.1,python-dateutil==2.8.2,python-slugify==6.1.2,PyYAML==5.4.1,requests==2.28.1,rich==12.4.4,ruamel.yaml==0.17.21,ruamel.yaml.clib==0.2.6,selinux==0.2.1,six==1.16.0,subprocess-tee==0.3.5,tenacity==8.0.1,text-unidecode==1.3,typing_extensions==4.3.0,urllib3==1.26.9,wcmatch==8.4,websocket-client==1.3.3,yamllint==1.26.3,zipp==3.8.0
py38-ansible210 run-test-pre: PYTHONHASHSEED='1972178064'
py38-ansible210 run-test: commands[0] | molecule test -s compatibility --destroy always
CRITICAL 'molecule/compatibility/molecule.yml' glob failed.  Exiting.
ERROR: InvocationError for command /opt/vector-role/.tox/py38-ansible210/bin/molecule test -s compatibility --destroy always (exited with code 1)
py38-ansible30 create: /opt/vector-role/.tox/py38-ansible30
py38-ansible30 installdeps: -rtox-requirements.txt, ansible<3.1
py38-ansible30 installed: ansible==3.0.0,ansible-base==2.10.17,ansible-compat==2.1.0,ansible-lint==5.1.3,arrow==1.2.2,attrs==21.4.0,bcrypt==3.2.2,binaryornot==0.4.4,bracex==2.3.post1,Cerberus==1.3.2,certifi==2022.6.15,cffi==1.15.1,chardet==5.0.0,charset-normalizer==2.1.0,click==8.1.3,click-help-colors==0.9.1,commonmark==0.9.1,cookiecutter==2.1.1,cryptography==37.0.4,distro==1.7.0,docker==5.0.3,enrich==1.2.7,idna==3.3,importlib-resources==5.8.0,Jinja2==3.1.2,jinja2-time==0.2.0,jmespath==1.0.1,jsonschema==4.6.2,lxml==4.9.1,MarkupSafe==2.1.1,molecule==3.4.0,molecule-docker==1.1.0,packaging==21.3,paramiko==2.11.0,pathspec==0.9.0,pluggy==0.13.1,pycparser==2.21,Pygments==2.12.0,PyNaCl==1.5.0,pyparsing==3.0.9,pyrsistent==0.18.1,python-dateutil==2.8.2,python-slugify==6.1.2,PyYAML==5.4.1,requests==2.28.1,rich==12.4.4,ruamel.yaml==0.17.21,ruamel.yaml.clib==0.2.6,selinux==0.2.1,six==1.16.0,subprocess-tee==0.3.5,tenacity==8.0.1,text-unidecode==1.3,typing_extensions==4.3.0,urllib3==1.26.9,wcmatch==8.4,websocket-client==1.3.3,yamllint==1.26.3,zipp==3.8.0
py38-ansible30 run-test-pre: PYTHONHASHSEED='1972178064'
py38-ansible30 run-test: commands[0] | molecule test -s compatibility --destroy always
CRITICAL 'molecule/compatibility/molecule.yml' glob failed.  Exiting.
ERROR: InvocationError for command /opt/vector-role/.tox/py38-ansible30/bin/molecule test -s compatibility --destroy always (exited with code 1)
________________________________________________________ summary ________________________________________________________
ERROR:   py38-ansible210: commands failed
ERROR:   py38-ansible30: commands failed
```
9. Добавьте новый тег на коммит с рабочим сценарием в соответствии с семантическим версионированием.

После выполнения у вас должно получится два сценария molecule и один tox.ini файл в репозитории. Ссылка на репозиторий являются ответами на домашнее задание. Не забудьте указать в ответе теги решений Tox и Molecule заданий.

## Необязательная часть

1. Проделайте схожие манипуляции для создания роли lighthouse.
2. Создайте сценарий внутри любой из своих ролей, который умеет поднимать весь стек при помощи всех ролей.
3. Убедитесь в работоспособности своего стека. Создайте отдельный verify.yml, который будет проверять работоспособность интеграции всех инструментов между ними.
4. Выложите свои roles в репозитории. В ответ приведите ссылки.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
