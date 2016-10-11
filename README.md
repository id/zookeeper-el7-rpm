zookeeper-redhat7-rpm
---------
A set of scripts to package zookeeper into an rpm.
Requires CentOS/RedHat 7.

Setup
-----
    sudo yum install make rpmdevtools

Building
--------
    make rpm

Resulting RPM will be avaliable at $(shell pwd)/noarch/

Installing and operating
------------------------
    sudo yum install zookeeper*.rpm
    sudo systemctl enable zookeeper
    sudo systemctl start zookeeper

Zookeeper shell is available via zkcli.

Default locations
-----------------
archives: /usr/share/java/zookeeper
data:     /var/lib/zookeeper
logs:     /var/log/zookeeper
configs:  /etc/zookeeper, /etc/sysconfig/zookeeper
