%define name keyutils
%define major 1

%define libname %mklibname %name %major
%define devname %mklibname -d %name
%define staticname %mklibname -d -s %name

Name:		%name
Version:	1.2
Release:	%mkrel 2
Summary:	Linux Key Management Utilities
URL:		http://people.redhat.com/~dhowells/keyutils/
Source:		http://people.redhat.com/~dhowells/keyutils/keyutils-%{version}.tar.bz2
Group:		System/Base
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

%build
%{make} ETCDIR=%{_sysconfdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} LIBDIR=/%{_lib} \
	USRLIBDIR=%{_libdir} SHAREDIR=%{_datadir}/%{name} INCLUDEDIR=%{_includedir}

%install
%{__rm} -Rf %{buildroot}
%{__make} ETCDIR=%{_sysconfdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} LIBDIR=/%{_lib} \
	  USRLIBDIR=%{_libdir} SHAREDIR=%{_datadir}/%{name} INCLUDEDIR=%{_includedir} \
	  DESTDIR=%{buildroot} install

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%doc README LICENCE.GPL LICENCE.LGPL
%config(noreplace) %{_sysconfdir}/request-key.conf
%{_bindir}/keyctl
%{_sbindir}/request-key
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

