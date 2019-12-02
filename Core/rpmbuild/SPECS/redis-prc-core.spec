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
# Extract binaries to BUILDROOT/cs/redis-prc
mkdir -p %{csroot}
tar -xvzf %{SOURCE0} -C %{csroot}

%files
%defattr(-, %user, %user_group, -)
%{csprefix}
