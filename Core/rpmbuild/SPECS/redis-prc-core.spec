Name: 		redis-prc
Version:	1.0.0
Vendor:		CS
Release:	%{?dist}
Packager:	mikhail.orlov@credit-suisse.com
Summary:	Installs Redis for PRC project
License:	Credit Suisse Internal
Source0:        redis-binaries.tar.gz

%global csprefix /cs/%{name}
%global csroot %{buildroot}%{csprefix}

%description
This installs Redis and makes basic configuration changes
on the Linux machine.

%prep
# Extract binaries to BUILD.
tar -xvzf %{SOURCE0} -C %{_builddir}

%build
# Nothing, as we don't compile anything.

%install
rm -rf %{buildroot}

# Prepare the binaries folder.
install -m 0755 -d %{csroot}/bin

# The files from the intermediate archive.
cp -lr bin/redis-* %{csroot}/bin/

%files
%defattr(-, %user, %user_group, -)
%{csprefix}
