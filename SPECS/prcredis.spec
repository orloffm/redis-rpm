Name:           PRC_Redis
Version:        1.0
Release:        1%{?dist}
Summary:        Redis for PRC

License:        Credit Suisse Internal
Source0:        http://download.redis.io/releases/redis-5.0.7.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

Requires:       logrotate

%description


%prep
%setup -q


%build
make %{?_smp_mflags} \
  DEBUG='' \
  CFLAGS='%{optflags}' \
  V=1 \
  all

%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=%{buildroot}%{_prefix}
# install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
# install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
# install -p -D -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
# install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
# install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
# install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}



%files
%doc


%clean
rm -fr %{buildroot}