# Домашнее задание к занятию "09.06 Gitlab"

ОТВЕТ, репозитарий Gitlab
https://aturganov.gitlab.yandexcloud.net/locadm/gitlab-test/-/tree/main
## Подготовка к выполнению

1. Необходимо [подготовить gitlab к работе по инструкции](https://cloud.yandex.ru/docs/tutorials/infrastructure-management/gitlab-containers)
2. Создайте свой новый проект
3. Создайте новый репозиторий в gitlab, наполните его [файлами](./repository)
4. Проект должен быть публичным, остальные настройки по желанию

```
Подключение к кластеру кубера через CLI:

yc managed-kubernetes cluster get-credentials cathuo4li1cf7m6gsogp --external --force

helm installed into /usr/local/bin/helm

[locadm@vds2295339 mnt-homeworks]$ kubectl cluster-info --kubeconfig /home/locadm/.kube/config
Kubernetes control plane is running at https://51.250.27.27
CoreDNS is running at https://51.250.27.27/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://51.250.27.27/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

Создание сервисного аккаунта kubectl apply -f gitlab-admin-service-account.yaml

kubectl apply -f gitlab-admin-service-account.yaml
serviceaccount/gitlab-admin created
Warning: rbac.authorization.k8s.io/v1beta1 ClusterRoleBinding is deprecated in v1.17+, unavailable in v1.22+; use rbac.authorization.k8s.io/v1 ClusterRoleBinding
clusterrolebinding.rbac.authorization.k8s.io/gitlab-admin created

Получение токена
[locadm@vds2295339 .kube]$ kubectl -n kube-system get secrets -o json | \
> jq -r '.items[] | select(.metadata.name | startswith("gitlab-admin")) | .data.token' | \
> base64 --decode
eyJhbGciOiJSUzI1NiIsImtpZCI6IjlWVVNoVDNTXzU3bFJBSGFsS0w0TEVpeWpKRVNuN0JGMV9FVmcyWU1JdDAifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJnaXRsYWItYWRtaW4tdG9rZW4tdGpxY3MiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZ2l0bGFiLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZGNjNzQ3ZWEtNjI0MS00Mjc0LWFlZjQtMzc3NWE0ZjQyYWM0Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmdpdGxhYi1hZG1pbiJ9.NT38ACaKYK2Z7ERdZl5iegSCvKnbLAmdt356Ssqhye_coOwm_sZAlg5biiM9R1FK7OoELa7Z4iu88UnOUBUE3vdnzDOzaFye9xm_4QwpBTvLQo95hc4dFS9l0d92J950r04PF2SBJlAauDdfT9uY8klV6hT56oU3sPTFzHDleJ5iatBsfrOKVJx9OfCiuFcihIt28gQcgm03Z2-XWRwpPQyblgWfPmVjOy4-66lEr31_aApTWoMjWj05cWFF4jRvf9pIXQi_mxOUFyaC3z8hKsRrzbqOPNWQ0F72AlynqI6xKLO1cXJ7jibttIUUMZWDUhm2aNmTQD5JIKad0zP1Sg[locadm@vds2295339 .kube]$ 


helm repo add gitlab https://charts.gitlab.io

Подключаем Runner в CLI
[locadm@vds2295339 helm]$ helm install --namespace default gitlab-runner -f values.yaml gitlab/gitlab-runner
NAME: gitlab-runner
LAST DEPLOYED: Sat Oct 29 21:30:05 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Your GitLab Runner should now be registered against the GitLab instance reachable at: "https://aturganov.gitlab.yandexcloud.net/"

Runner namespace "default" was found in runners.config template.

yc managed-kubernetes cluster get cathuo4li1cf7m6gsogp --format=json \
  | jq -r .master.endpoints.external_v4_endpoint
https://51.250.27.27

Создал в кластере узлы
[locadm@vds2295339 helm]$ yc managed-kubernetes cluster list-nodes --id cathuo4li1cf7m6gsogp
+--------------------------------+-----------------+--------------------------------+-------------+---------------+
|         CLOUD INSTANCE         | KUBERNETES NODE |           RESOURCES            |    DISK     |    STATUS     |
+--------------------------------+-----------------+--------------------------------+-------------+---------------+
| epds3ekb913bqsrlo509           |                 | 2 100% core(s), 4.0 GB of      | 96.0 GB hdd | NOT_CONNECTED |
| RUNNING_ACTUAL                 |                 | memory                         |             |               |
+--------------------------------+-----------------+--------------------------------+-------------+---------------+

Жду запуска подов
[locadm@vds2295339 helm]$ kubectl get pods -n default | grep gitlab-runner
gitlab-runner-754c695b59-2bp5k                1/1     Running           0          59m
```

!['Снимок10.PNG'](Снимок10.PNG)
![](vscode-remote://ssh-remote%2Bihor/home/locadm/git/mnt-homeworks/09-ci-06-gitlab/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA10.PNG)


```
Просмотр default service account
[locadm@vds2295339 .kube]$ kubectl get sa default -o yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2022-10-29T16:33:25Z"
  name: default
  namespace: default
  resourceVersion: "339"
  uid: fea96a82-67d4-40b0-9d52-1940c3d0fcfa
secrets:
- name: default-token-phczp
```
хмммм...
Ошибка  is forbidden: User "system:serviceaccount:default:default" cannot get resource "deployments" in API group "apps" in the namespace
была исправлена спустя 4 часа вот такой командой :(
https://devops.stackexchange.com/questions/8047/helm-cannot-get-resource-namespaces-in-api-group
```
kubectl create clusterrolebinding default --clusterrole cluster-admin --serviceaccount=default:default
```
## Основная часть

### DevOps

В репозитории содержится код проекта на python. Проект - RESTful API сервис. Ваша задача автоматизировать сборку образа с выполнением python-скрипта:
1. Образ собирается на основе [centos:7](https://hub.docker.com/_/centos?tab=tags&page=1&ordering=last_updated)
2. Python версии не ниже 3.7
3. Установлены зависимости: `flask` `flask-jsonpify` `flask-restful`
4. Создана директория `/python_api`
5. Скрипт из репозитория размещён в /python_api
6. Точка вызова: запуск скрипта
7. Если сборка происходит на ветке `master`: должен подняться pod kubernetes на основе образа `python-api`, иначе этот шаг нужно пропустить



### Product Owner

Вашему проекту нужна бизнесовая доработка: необходимо поменять JSON ответа на вызов метода GET `/rest/api/get_info`, необходимо создать Issue в котором указать:
1. Какой метод необходимо исправить
2. Текст с `{ "message": "Already started" }` на `{ "message": "Running"}`
3. Issue поставить label: feature


!['Снимок12.PNG'](Снимок12.PNG)

### Developer

Вам пришел новый Issue на доработку, вам необходимо:
1. Создать отдельную ветку, связанную с этим issue
2. Внести изменения по тексту из задания
3. Подготовить Merge Requst, влить необходимые изменения в `master`, проверить, что сборка прошла успешно

!['Снимок13.PNG'](Снимок13.PNG)
### Tester

Разработчики выполнили новый Issue, необходимо проверить валидность изменений:
1. Поднять докер-контейнер с образом `python-api:latest` и проверить возврат метода на корректность
2. Закрыть Issue с комментарием об успешности прохождения, указав желаемый результат и фактически достигнутый

## Итог

После успешного прохождения всех ролей - отправьте ссылку на ваш проект в гитлаб, как решение домашнего задания

https://aturganov.gitlab.yandexcloud.net/locadm/gitlab-test/-/tree/main

### :bangbang: Не забудьте оставить GitLab рабочим после выполнения задания и погасить все ресурсы в Yandex.Cloud сразу после получения зачета по домашнему заданию.

## Необязательная часть

Автомазируйте работу тестировщика, пусть у вас будет отдельный конвейер, который автоматически поднимает контейнер и выполняет проверку, например, при помощи curl. На основе вывода - будет приниматься решение об успешности прохождения тестирования



