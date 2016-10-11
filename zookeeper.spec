%define __jar_repack 0
#define debug_package %{nil}
%define zk_prefix     %{_javadir}/zookeeper
%define zk_confdir    %{_sysconfdir}/zookeeper
%define zk_logdir     %{_var}/log/zookeeper
%define zk_datadir    %{_sharedstatedir}/zookeeper

Summary: High-performance coordination service for distributed applications
Name: zookeeper
#Version: %{version}
#Release: %{release}%{?dist}
Version: 3.4.9
Release: 1%{?dist}
License: ASL 2.0 and BSD
Group: Applications/Databases
URL: https://zookeeper.apache.org/
Source0: https://www.apache.org/dyn/closer.cgi/zookeeper/zookeeper-%{version}/zookeeper-%{version}.tar.gz
Source1: zookeeper.service
Source2: zkcli
Source3: zookeeper.logrotate
Source4: zookeeper.sysconfig
Source5: zoo.cfg
Source6: log4j.properties
Source7: log4j-cli.properties
%{?systemd_requires}
BuildRequires: systemd
BuildArch: noarch

%description
ZooKeeper is a high-performance coordination service for distributed
applications. It exposes common services - such as naming, configuration
management, synchronization, and group services - in a simple interface so
you don't have to write them from scratch. You can use it off-the-shelf to
implement consensus, group management, leader election, and presence
protocols. And you can build on it for your own, specific needs.

%prep
%setup -q

%build

%install
# JARs
mkdir -p $RPM_BUILD_ROOT%{zk_prefix}
install -p -m 0644 zookeeper-%{version}.jar lib/*.jar \
  $RPM_BUILD_ROOT%{zk_prefix}/
# Service, systemd fails to expand file paths in runtime
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
CLASSPATH=
for i in $RPM_BUILD_ROOT%{zk_prefix}/*.jar; do
  CLASSPATH="%{zk_prefix}/$(basename ${i}):${CLASSPATH}"
done
sed -e "s|@CLASSPATH@|${CLASSPATH}|" %{S:1} > \
  $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service
# CLI
install -p -D -m 0755 %{S:2} $RPM_BUILD_ROOT%{_bindir}/zkcli
# Configuration
install -p -D -m 0644 %{S:3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zookeeper
install -p -D -m 0644 %{S:4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/zookeeper
mkdir -p $RPM_BUILD_ROOT%{zk_confdir}/
install -p -m 0644 %{S:5} %{S:6} %{S:7} conf/configuration.xsl \
  $RPM_BUILD_ROOT%{zk_confdir}/
# Empty directories
mkdir -p $RPM_BUILD_ROOT%{zk_logdir}
mkdir -p $RPM_BUILD_ROOT%{zk_datadir}

%pre
/usr/bin/getent group zookeeper >/dev/null || /usr/sbin/groupadd -r zookeeper
if ! /usr/bin/getent passwd zookeeper >/dev/null; then
  /usr/sbin/useradd -r -g zookeeper -M -N -d %{zk_prefix} -s /bin/bash -c "Zookeeper" zookeeper
fi

%post
%systemd_post zookeeper.service

%preun
%systemd_preun zookeeper.service

%postun
%systemd_postun_with_restart zookeeper.service

%files
%license LICENSE.txt
%{zk_prefix}/
%{_unitdir}/zookeeper.service
%{_bindir}/zkcli
%config(noreplace) %{_sysconfdir}/logrotate.d/zookeeper
%config(noreplace) %{_sysconfdir}/sysconfig/zookeeper
%dir %{zk_confdir}/
%config(noreplace) %{zk_confdir}/*
%attr(0755,zookeeper,zookeeper) %dir %{zk_logdir}/
%attr(0700,zookeeper,zookeeper) %dir %{zk_datadir}/

