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
%global our_user prcuser
%global our_group prcgroup

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

# redis-prc.service -> /cs/redis-prc/lib/redis-prc.service
install -p -D -m 644 %{name}.service %{csroot}/lib/%{name}.service

# redis-prc-shutdown.sh -> /cs/redis-prc/libexec/redis-prc-shutdown.sh
install -p -D -m 755 %{name}-stop.sh %{csroot}/libexec/%{name}-stop.sh

%files
%defattr(-, %our_user, %our_group, -)
%{csprefix}

# Installation scripts

%pre
# Check user and group exist.
(id %{our_user}) >/dev/null 2>&1 || {
  echo "User %{our_user} does not exist.
  exit 1
}
(id -g %{our_group}) >/dev/null 2>&1 || {
  echo "Group %{our_group} does not exist.
  exit 1
}
if [ ! -d /cs/%{our_user} ]; then
  echo "Directory /cs/%{our_user} does not exist.
  exit 1
fi

# Needed.
echo 1 > /proc/sys/vm/overcommit_memory
echo madvise > /sys/kernel/mm/transparent_hugepage/enabled

# Setup home folder.
mkdir -p /cs/%{our_user}/redis
chmod -hR %{our_user}:%{our_group} /cs/%{our_user}/redis

%post
if [ $1 -eq 1 ]; then
  # Initial install.
  systemctl preset %{csroot}/lib/%{name}.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ]; then
  # Removal, not upgrade.
  systemctl --no-reload disable redis-prc.service > /dev/null 2>&1 || :
  systemctl stop %{name}.service > /dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ]; then
  # Upgrade, not uninstall.
  systemctl try-restart %{name}.service > /dev/null 2>&1 || :
fi
