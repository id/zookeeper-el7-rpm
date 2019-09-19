# default build is for CentOS7, change the base image to fit your build.
FROM centos:centos7
MAINTAINER Sebastien Le Digabel "sledigabel@gmail.com"

RUN yum install -y wget make rpmdevtools

ADD Makefile zookeeper.logrotate zookeeper.service zookeeper.spec zookeeper.sysconfig zookeeper.log4j.properties zookeeper.log4j-cli.properties zkcli zoo.cfg /root/

RUN mkdir /root/RPMS

WORKDIR /root

VOLUME ["/root/RPMS"]

CMD make
