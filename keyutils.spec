%define major 1
%define oldlibname %mklibname %{name} 1
%define libname %mklibname %{name}
%define devname %mklibname -d %{name}
%define static %mklibname -d -s %{name}
%global build_ldflags %{build_ldflags} -Wl,--undefined-version

Summary:	Linux Key Management Utilities
Name:		keyutils
Version:	1.6.1
Release:	4
Group:		System/Base
License:	LGPLv2+
Url:		http://people.redhat.com/~dhowells/keyutils/
Source0:	http://people.redhat.com/~dhowells/keyutils/%{name}-%{version}.tar.bz2
Patch0:		keyutils-request-key-conf-add-cifs.upcall.patch
BuildRequires:	kernel-headers

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to userspace to get a key
instantiated.

%package -n %{libname}
Summary:	Linux Key Management Utilities
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
Librarie to control the kernel key management facility and to provide
a mechanism by which the kernel call back to userspace to get a key
instantiated.

%package -n %{devname}
Summary:	Developement files for %{libname}
Group:		System/Libraries
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Developement files for %{libname}.

%prep
%autosetup -p1

%build
%make_build \
	CC=%{__cc} \
	ETCDIR=%{_sysconfdir} \
	BINDIR=%{_bindir} \
	SBINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} \
	USRLIBDIR=%{_libdir} \
	SHAREDIR=%{_datadir}/%{name} \
	INCLUDEDIR=%{_includedir} \
	CFLAGS="%{optflags}" \
	LDFLAGS="%{build_ldflags}"

%install
%make_install \
	NO_ARLIB=1 \
	ETCDIR=%{_sysconfdir} \
	BINDIR=%{_bindir} \
	SBINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} \
	USRLIBDIR=%{_libdir} \
	SHAREDIR=%{_datadir}/%{name} \
	INCLUDEDIR=%{_includedir}

%files
%doc README
%config(noreplace) %{_sysconfdir}/request-key.conf
%{_bindir}/keyctl
%{_sbindir}/request-key
%{_sbindir}/key.dns_resolver
%doc %{_mandir}/man1/keyctl.1.*
%doc %{_mandir}/man5/request-key.conf.5.*
%doc %{_mandir}/man8/request-key.8.*
%doc %{_mandir}/man8/key.dns_resolver.8*
%{_datadir}/%{name}/request-key-debug.sh

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*.pc
%doc %{_mandir}/man3/*.3.*
%doc %{_mandir}/man7/*.7.*
