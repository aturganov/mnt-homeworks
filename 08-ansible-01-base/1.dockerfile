FROM centos:7


LABEL label="centos7"

RUN yum -y install epel-release
RUN yum -y update
RUN yum -y install nginx

ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]