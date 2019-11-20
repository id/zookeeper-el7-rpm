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

or use Docker

    docker build -t zookeeper-build . && docker run -ti -v $(pwd)/RPMS:/root/RPMS zookeeper-build

Resulting RPM will be avaliable at $(shell pwd)/RPMS/x86_64

Installing and operating
------------------------
    sudo yum install zookeeper*.rpm
    sudo systemctl start zookeeper
    sudo systemctl enable zookeeper

Zookeeper shell is available via /usr/local/bin/zkcli or just zkcli since /usr/local/bin is usually in the $PATH.

Default locations
-----------------
binaries: /opt/zookeeper  
data:     /var/lib/zookeeper  
logs:     /var/log/zookeeper  
configs:  /etc/zookeeper, /etc/sysconfig/zookeeper  
