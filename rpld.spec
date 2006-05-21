Summary:	RPLD implements the IBM RIPL protocol
Summary(pl):	RPLD jest implementacja protoko³u RIPL firmy IBM
Name:		rpld
Version:	1.7
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://gimel.esc.cam.ac.uk/james/rpld/src/%{name}-%{version}.tar.gz
# Source0-md5:	933e1bec097595c1a7bf805f9d735a5b
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-build.patch
URL:		http://gimel.esc.cam.ac.uk/james/rpld/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rpld will net-boot IBM style RPL boot ROMs.

%description -l pl
RPLD jest implementacja protoko³u RIPL firmy IBM.

%prep
%setup -q
%patch0 -p1

%build
%{__make} depend
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},%{_sysconfdir},/etc/{rc.d/init.d,sysconfig},%{_mandir}/man{5,8}}

install {rpld,ana} $RPM_BUILD_ROOT%{_sbindir}
install rpld.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/rpld.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rpld
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rpld
install rpld.8 $RPM_BUILD_ROOT%{_mandir}/man8
install rpld.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rpld
%service rpld restart "RPL daemon"

%preun
if [ "$1" = "0" ]; then
	%service rpld stop
	/sbin/chkconfig --del rpld
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpld.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rpld
%attr(755,root,root) %{_sbindir}/rpld
%attr(755,root,root) %{_sbindir}/ana
%attr(754,root,root) /etc/rc.d/init.d/rpld
%{_mandir}/man[58]/*
