Name:             redis
Version:          5.0.7
Release:          1%{?dist}
Summary:          A persistent key-value database

Group:            Applications/Databases
License:          BSD
URL:              http://redis.io
Source0:          http://download.redis.io/releases/%{name}-%{version}.tar.gz
#Source1:          %{name}.logrotate
#Source2:          %{name}.init
# Update configuration
#Patch0:           %{name}-2.4.8-redis.conf.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}

ExcludeArch:      ppc ppc64

Requires:         logrotate
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(pre):    shadow-utils
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

%prep
%setup -q
#%patch0 -p1

%build
make %{?_smp_mflags} \
  DEBUG='' \
  CFLAGS='%{optflags}' \
  V=1 \
  all

%install
rm -fr %{buildroot}
make install PREFIX=%{buildroot}%{_prefix}
# Install misc other
#install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
#install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
#install -p -D -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
#install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
#install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
#install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

# Fix non-standard-executable-perm error
chmod 755 %{buildroot}%{_bindir}/%{name}-*

# Ensure redis-server location doesn't change
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/%{name}-server %{buildroot}%{_sbindir}/%{name}-server

%clean
rm -fr %{buildroot}

#%post
#/sbin/chkconfig --add redis

# %pre
# getent group redis &> /dev/null || groupadd -r redis &> /dev/null
# getent passwd redis &> /dev/null || \
# useradd -r -g redis -d %{_localstatedir}/lib/redis -s /sbin/nologin \
# -c 'Redis Server' redis &> /dev/null
# exit 0

%preun
#if [ $1 = 0 ]; then
#  /sbin/service redis stop &> /dev/null
#  /sbin/chkconfig --del redis &> /dev/null
#fi

%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %attr(0755, redis, root) %{_localstatedir}/lib/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-*
%{_sbindir}/%{name}-*
%{_initrddir}/%{name}