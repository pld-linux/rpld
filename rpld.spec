Summary:	RPLD implements the IBM RIPL protocol.
Summary(pl):	RPLD jest implementacja protoko³u RIPL firmy IBM
Name:		rpld
Version:	1.7
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	%{name}-%{version}.tar.gz
Source1:	rpld.init
Source2:	rpld.sysconfig
URL:		http://gimel.esc.cam.ac.uk/james/rpld
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description


%prep
%setup  -q

%build
%{__make} depend
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},/etc/{rc.d/init.d,sysconfig},%{_mandir}/man{5,8}}

cp {rpld,ana} $RPM_BUILD_ROOT%{_sbindir}
cp rpld.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/rpld.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rpld
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rpld
cp rpld.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp rpld.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5

gzip -9nf INSTALL LICENCE README

%pre

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rpld ]; then
		/etc/rc.d/init.d/rpld stop 1>&2
	fi
	/sbin/chkconfig --del rpld
fi
					

%post
/sbin/chkconfig --add rpld
if [ -f /var/lock/subsys/rpld ]; then
	/etc/rc.d/init.d/rpld restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/rpld start\" to start RPL daemon."
fi
		
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/rpld.conf
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/rpld
%attr(755,root,root) %{_sbindir}/rpld
%attr(755,root,root) %{_sbindir}/ana
%attr(754,root,root) /etc/rc.d/init.d/rpld

%{_mandir}/man5/*
%{_mandir}/man8/*

%doc {INSTALL,LICENCE,README}.gz
