Name: 		redis-prc
Version:	1.0.0
Vendor:		CS
Release:	%{?dist}
Packager:	mikhail.orlov@credit-suisse.com
Summary:	Installs Redis for PRC project
License:	Credit Suisse Internal
Source0:        redis-binaries.tar.gz
Source1:	redis.conf

%global csprefix /cs/%{name}
%global csroot %{buildroot}%{csprefix}

%description
This installs Redis and makes basic configuration changes
on the Linux machine.

%prep
# Extract binaries to BUILD.
tar -xvzf %{SOURCE0} -C %{_builddir}
cp %{SOURCE1} %{_builddir}

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

%files
%defattr(-, %user, %user_group, -)
%{csprefix}
