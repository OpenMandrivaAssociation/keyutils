%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}
%define	staticname %mklibname -d -s %{name}

Summary:	Linux Key Management Utilities
Name:		keyutils
Version:	1.5.5
Release:	2
URL:		http://people.redhat.com/~dhowells/keyutils/
Source0:	http://people.redhat.com/~dhowells/keyutils/%{name}-%{version}.tar.bz2
Patch0:		keyutils-request-key-conf-add-cifs.upcall.patch
Group:		System/Base
License:	LGPLv2+

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to userspace to get a key
instantiated.

%package -n	%{libname}
Summary:	Linux Key Management Utilities
Group:		System/Libraries

%description -n	%{libname}
Librarie to control the kernel key management facility and to provide
a mechanism by which the kernel call back to userspace to get a key
instantiated.

%package -n	%{devname}
Summary:	Developement files for %libname
Group:		System/Libraries
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
Developement files for %{libname}.

%prep
%setup -q
%patch0 -p1

%build
%make -j1 ETCDIR=%{_sysconfdir} BINDIR=/bin SBINDIR=/sbin LIBDIR=/%{_lib} \
	USRLIBDIR=%{_libdir} SHAREDIR=%{_datadir}/%{name} INCLUDEDIR=%{_includedir} \
	CFLAGS='%{optflags}' LDFLAGS="%{ldflags}"

%install
%makeinstall_std ETCDIR=%{_sysconfdir} BINDIR=/bin SBINDIR=/sbin LIBDIR=/%{_lib} \
	  USRLIBDIR=%{_libdir} SHAREDIR=%{_datadir}/%{name} INCLUDEDIR=%{_includedir}

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files
%doc README LICENCE.GPL LICENCE.LGPL
%config(noreplace) %{_sysconfdir}/request-key.conf
/bin/keyctl
/sbin/request-key
/sbin/key.dns_resolver
%{_mandir}/man1/keyctl.1.*
%{_mandir}/man5/request-key.conf.5.*
%{_mandir}/man8/request-key.8.*
%{_mandir}/man8/key.dns_resolver.8*
%{_datadir}/%{name}/request-key-debug.sh

%files -n %{libname}
/%{_lib}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_mandir}/man3/*.3.*
