Name: 		redis-prc
Version:	1.0.0
Vendor:		CS
Release:	%{?dist}
Packager:	mikhail.orlov@credit-suisse.com
Summary:	Installs Redis for PRC project
License:	Credit Suisse Internal
Source0:        redis-binaries.tar.gz
Source1:	redis.conf
Source2:	%{name}.service
Source3:	%{name}-stop.sh

%global csprefix /cs/%{name}
%global csroot %{buildroot}%{csprefix}

%description
This installs Redis and makes basic configuration changes
on the Linux machine.

%prep
# Extract binaries to BUILD.
tar -xvzf %{SOURCE0} -C %{_builddir}

# Copy files from SOURCES to BUILD.
cp %{SOURCE1} %{_builddir}
cp %{SOURCE2} %{_builddir}
cp %{SOURCE3} %{_builddir}

%build
# Nothing, as we don't compile anything.

%install
rm -rf %{buildroot}

# Prepare the binaries folder.
install -m 0755 -d %{csroot}/bin

# The files from the intermediate archive.
# redis-* -> /cs/redis-prc/bin/redis-*
cp -lr bin/redis-* %{csroot}/bin/

# redis.conf -> /cs/redis-prc/etc/redis.conf
install -p -D -m 644 redis.conf %{csroot}%{_sysconfdir}/redis.conf

# redis-prc.service -> /cs/redis-prc/usr/lib/systemd/system/redis-prc.service
install -p -D -m 644 %{name}.service %{csroot}%{_libdir}/systemd/system/%{name}.service

# redis-prc-shutdown.sh -> /cs/redis-prc/usr/libexec/redis-prc-shutdown.sh
install -p -D -m 755 %{name}-stop.sh %{csroot}%{_libexecdir}/%{name}-stop.sh

# Create /cs/redis-prc/var/log/redis
install -d -m 755 %{csroot}%{_localstatedir}/log

%files
%defattr(-, %user, %user_group, -)
%{csprefix}
