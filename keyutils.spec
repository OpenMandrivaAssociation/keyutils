%define major 1
%define oldlibname %mklibname %{name} 1
%define libname %mklibname %{name}
%define devname %mklibname -d %{name}
%define static %mklibname -d -s %{name}
%global build_ldflags %{build_ldflags} -Wl,--undefined-version

Summary:	Linux Key Management Utilities
Name:		keyutils
Version:	1.6.3
Release:	1
Group:		System/Base
License:	LGPLv2+
Url:		https://people.redhat.com/~dhowells/keyutils/
Source0:	https://git.kernel.org/pub/scm/linux/kernel/git/dhowells/keyutils.git/snapshot/keyutils-%{version}.tar.gz
#Source0:	http://people.redhat.com/~dhowells/keyutils/%{name}-%{version}.tar.bz2
Patch0:		keyutils-request-key-conf-add-cifs.upcall.patch
BuildRequires:	make
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
	CC="%{__cc}" \
	ETCDIR="%{_sysconfdir}" \
	BINDIR="%{_bindir}" \
	SBINDIR="%{_sbindir}" \
	LIBDIR="%{_libdir}" \
	USRLIBDIR="%{_libdir}" \
	SHAREDIR="%{_datadir}/%{name}" \
	INCLUDEDIR="%{_includedir}" \
	CFLAGS="%{optflags}" \
	LDFLAGS="%{build_ldflags}"

%install
%make_install \
	NO_ARLIB=1 \
	ETCDIR="%{_sysconfdir}" \
	BINDIR="%{_bindir}" \
	SBINDIR="%{_sbindir}" \
	LIBDIR="%{_libdir}" \
	USRLIBDIR="%{_libdir}" \
	SHAREDIR="%{_datadir}/%{name}" \
	INCLUDEDIR="%{_includedir}"

# The libkeyutils.so symlink always points at /usr/lib64/libkeyutils.so.%{major},
# even if we're installing to /usr/loongarch64-openmandriva-linux-gnu/lib64...
# Make it relative
rm %{buildroot}%{_libdir}/libkeyutils.so
ln -s libkeyutils.so.%{major} %{buildroot}%{_libdir}/libkeyutils.so

%files
%doc README
%config(noreplace) %{_sysconfdir}/request-key.conf
%{_bindir}/keyctl
%{_sbindir}/request-key
%{_sbindir}/key.dns_resolver
%doc %{_mandir}/man1/keyctl.1*
%doc %{_mandir}/man5/request-key.conf.5*
%doc %{_mandir}/man8/request-key.8*
%doc %{_mandir}/man8/key.dns_resolver.8*
%{_datadir}/%{name}/request-key-debug.sh

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*.pc
%doc %{_mandir}/man3/*.3*
%doc %{_mandir}/man7/*.7*
%doc %{_mandir}/man5/key.dns_resolver.conf.5*
