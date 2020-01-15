%global __jar_repack 0
%global zk_prefix  %{_javadir}/zookeeper
%global zk_confdir %{_sysconfdir}/zookeeper
%global zk_logdir  %{_var}/log/zookeeper
%global zk_datadir %{_sharedstatedir}/zookeeper

%{!?zk_name:%global zk_name zookeeper}
%{!?zk_version:%global zk_version 3.4.14}
%{!?zk_release:%global zk_release 1}

Summary: High-performance coordination service for distributed applications
Name: %{zk_name}
Version: %{zk_version}
Release: %{zk_release}%{?dist}
License: ASL 2.0 and BSD
Group: Applications/Databases
URL: https://zookeeper.apache.org/
Source0: https://www-eu.apache.org/dist/zookeeper/zookeeper-%{version}/zookeeper-%{version}.tar.gz
Source1: zookeeper.service
Source2: zookeeper.logrotate
Source3: zoo.cfg
Source4: zookeeper.log4j.properties
Source5: zookeeper.log4j-cli.properties
Source6: zookeeper.sysconfig
Source7: zkcli
%{?systemd_requires}
BuildArch: noarch
Requires: java-headless

%description
ZooKeeper is a high-performance coordination service for distributed
applications. It exposes common services - such as naming, configuration
management, synchronization, and group services - in a simple interface so
you don't have to write them from scratch. You can use it off-the-shelf to
implement consensus, group management, leader election, and presence
protocols. And you can build on it for your own, specific needs.

%package -n nagios-plugins-zookeeper
Group: Applications/System
Summary: Provides check_zookeeper support for Nagios
Requires: nagios-plugins

%description -n nagios-plugins-zookeeper
Provides check_zookeeper support for Nagios.

%prep
%setup -q -n zookeeper-%{version}

%build

%install
# JARs
mkdir -p $RPM_BUILD_ROOT%{zk_prefix}
install -p -m 0644 zookeeper-%{version}.jar lib/*.jar \
  $RPM_BUILD_ROOT%{zk_prefix}/
# Service, systemd fails to expand file paths in runtime
install -p -D -m 0644 %{S:1} $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
# Configuration
install -p -D -m 0644 %{S:2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zookeeper
install -p -D -m 0644 %{S:3} $RPM_BUILD_ROOT%{zk_confdir}/zoo.cfg
install -p -D -m 0644 %{S:4} $RPM_BUILD_ROOT%{zk_confdir}/log4j.properties
install -p -D -m 0644 %{S:5} $RPM_BUILD_ROOT%{zk_confdir}/log4j-cli.properties
install -p -D -m 0644 %{S:6} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/zookeeper
# CLI
install -p -D -m 0755 %{S:7} $RPM_BUILD_ROOT%{_bindir}/zkcli
# Empty directories
mkdir -p $RPM_BUILD_ROOT%{zk_logdir}
mkdir -p $RPM_BUILD_ROOT%{zk_datadir}
# Nagios plugin, enforce python2 for RHEL8
install -D -p -m 0755 \
  zookeeper-contrib/zookeeper-contrib-monitoring/check_zookeeper.py \
  $RPM_BUILD_ROOT%{_libdir}/nagios/plugins/check_zookeeper
sed -i -e 's/python$/python2/g' \
  $RPM_BUILD_ROOT%{_libdir}/nagios/plugins/check_zookeeper

%pre
/usr/bin/getent group zookeeper >/dev/null || /usr/sbin/groupadd -r zookeeper
if ! /usr/bin/getent passwd zookeeper >/dev/null ; then
    /usr/sbin/useradd -r -g zookeeper -M -d %{_prefix}/zookeeper -s /bin/bash -c "Zookeeper" zookeeper
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

%files -n nagios-plugins-zookeeper
%{_libdir}/nagios/plugins/check_zookeeper

