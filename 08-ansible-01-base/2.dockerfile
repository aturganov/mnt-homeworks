FROM ubuntu:latest


LABEL label="ubuntu"

RUN apt-get -y update
RUN apt-get -y install nginx

RUN apt-get -y install python3
# RUN apt-get -y install python

ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]
