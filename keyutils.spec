%define name keyutils
%define major 1

%define libname %mklibname %name %major
%define devname %mklibname -d %name
%define staticname %mklibname -d -s %name

Name:		%name
Version:	1.2
Release:	%mkrel 13
Summary:	Linux Key Management Utilities
URL:		http://people.redhat.com/~dhowells/keyutils/
Source:		http://people.redhat.com/~dhowells/keyutils/keyutils-%{version}.tar.bz2
Patch:		keyutils-request-key-conf-add-cifs.upcall.patch
Group:		System/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	LGPLv2+
%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to userspace to get a key
instantiated.

%package -n %libname
Summary:	Linux Key Management Utilities
Group:		System/Libraries
%description -n %libname
Librarie to control the kernel key management facility and to provide
a mechanism by which the kernel call back to userspace to get a key
instantiated.

%package -n %devname
Summary:	Developement files for %libname
Group:		System/Libraries
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
%description -n %devname
Developement files for %libname

%package -n %staticname
Summary:	%name static library
Group:		System/Libraries
Requires:	%devname
%description -n %staticname
%name static library.

%prep
%setup -q
%patch -p1

%build
%{make} -j1 ETCDIR=%{_sysconfdir} BINDIR=/bin SBINDIR=/sbin LIBDIR=/%{_lib} \
	USRLIBDIR=%{_libdir} SHAREDIR=%{_datadir}/%{name} INCLUDEDIR=%{_includedir} \
	CFLAGS='%optflags'

%install
%{__rm} -Rf %{buildroot}
%{__make} ETCDIR=%{_sysconfdir} BINDIR=/bin SBINDIR=/sbin LIBDIR=/%{_lib} \
	  USRLIBDIR=%{_libdir} SHAREDIR=%{_datadir}/%{name} INCLUDEDIR=%{_includedir} \
	  DESTDIR=%{buildroot} install

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%doc README LICENCE.GPL LICENCE.LGPL
%config(noreplace) %{_sysconfdir}/request-key.conf
/bin/keyctl
/sbin/request-key
%{_mandir}/man1/keyctl.1.*
%{_mandir}/man5/request-key.conf.5.*
%{_mandir}/man8/request-key.8.*
%{_datadir}/%{name}/request-key-debug.sh

%files -n %libname
/%{_lib}/lib%{name}-%{version}.so
/%{_lib}/lib%{name}.so.%{major}

%files -n %devname
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_mandir}/man3/*.3.*

%files -n %staticname
%{_libdir}/lib%{name}.a



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2-12mdv2011.0
+ Revision: 666026
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2-11mdv2011.0
+ Revision: 606262
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2-10mdv2010.1
+ Revision: 519014
- rebuild

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.2-9mdv2010.0
+ Revision: 425484
- rebuild

* Tue Nov 25 2008 Nicolas Vigier <nvigier@mandriva.com> 1.2-8mdv2009.1
+ Revision: 306648
- keyctl should be in /bin (as referenced in /etc/request-key.conf)

* Tue Nov 25 2008 Pascal Terjan <pterjan@mandriva.org> 1.2-7mdv2009.1
+ Revision: 306641
- request-key needs to be in /sbin (the kernel want it there)

* Thu Oct 30 2008 Buchan Milne <bgmilne@mandriva.org> 1.2-6mdv2009.1
+ Revision: 298767
- Disable parallel build (breaks on smp if -devel package not installed)

* Wed Oct 29 2008 Buchan Milne <bgmilne@mandriva.org> 1.2-5mdv2009.1
+ Revision: 298578
- Add lines to /etc/request-key.conf for cifs.upcall required for krb5
  support for mount.cifs

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 1.2-4mdv2009.0
+ Revision: 247744
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 1.2-2mdv2008.1
+ Revision: 168032
- fix no-buildroot-tag

* Thu Sep 06 2007 Nicolas Vigier <nvigier@mandriva.com> 1.2-2mdv2008.0
+ Revision: 80748
- build with optflags
- run ldconfig

* Thu Sep 06 2007 Nicolas Vigier <nvigier@mandriva.com> 1.2-1mdv2008.0
+ Revision: 80726
- Import keyutils

