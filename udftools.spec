

%define name    udftools
%define version	1.0.0
%define beta	b3
%define tarver	%{version}%{beta}cvs20040419
%define mdkrel	%mkrel 13


%if %beta
%define release 0.%{beta}.%{mdkrel}
%else
%define release %{mdkrel}
%endif

%define major 1
%define libname %mklibname udftools %{major}
%define develname %mklibname -d udftools
%define sdevelname %mklibname -d -s udftools


Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPLv2+
Group:		System/Kernel and hardware
Provides:	udf
Obsoletes:	udf
Autoreqprov:	off
Summary:	UDF filesystem tools
Source:		%{name}-%{tarver}.tar.bz2
Source1:	pktcdvd.init.d.bz2
Source2:	pktcdvd.sysconfig.bz2
Source3:	pktcdvd.html.bz2
Source4:	pktcdvd-hint.txt.bz2
#Patch1:		udftool}s-%{cvsrelease}.patch.bz2
Patch2:		udftools-disable_broken.patch 
Patch3:		udftools-1.0.0b3cvs_add_cdmrw.patch
Patch4:		udftools-1.0.0b3-kernel-2.6.8.1.patch
Patch5:         udftools-1.0.0-gcc4.patch
Patch6:		udftools-open.patch
URL:		http://sourceforge.net/projects/linux-udf/
BuildRoot:	%{_tmppath}/%{name}-%{version}%{beta}-build
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Requires:	%{libname} = %version-%release
BuildRequires:	autoconf automake
BuildRequires:	readline-devel
BuildRequires:  ncurses-devel

%description -n udftools
These are tools for UDF file systems as used, e.g.,
on DVD-RAM, DVD+RW, CD-RW. They are also used for
managing Packet-CD/DVD devices and media.


%package -n %{libname}
Summary:	Libraries from %name
Group:		System/Libraries
Provides:	%{libname} = %version-%release
Provides:	libudftools = %version-%release

%description -n %{libname}
This package contains the libraries meeded by %name.


%package -n %{develname}
Summary:	Devel files from %name
Group:		Development/C
Requires:	%{libname} = %version-%release
Provides:	libudftools-devel = %version-%release
Provides:	%name-devel = %version-%release
Provides:	%{libname}-devel = %version-%release
Obsoletes:	%mklibname -d udftools 1

%description -n %{develname}
This is the libraries, include files and other resources you can use
to incorporate %name into applications.

%package -n %sdevelname
Summary:	Static Library for developing applications with %name
Group:		Development/C
Requires:	%develname = %epoch:%version-%release
Provides:	udftools-static-devel = %version-%release
Obsoletes:	%mklibname -d -s udftools 1

%description -n %sdevelname
This contains the static library of %name needed for building apps that
link statically to %name.

%prep
%setup -q -n %{name}
#{version}%{beta}
#patch1
#patch2 -p1
%patch3 -p1
%patch4 -p1 -b .kernel-2.6.8.1
%patch5 -p1 -b .gcc4
%patch6 -p0
perl -pi -e 's! udfct/Makefile! udfct/Makefile cdmrw/Makefile!' configure.in
perl -pi -e 's! udfct! udfct cdmrw!' Makefile.am

%build
autoreconf --force --install
%configure2_5x --enable-shared
%make

%install
rm -Rf $RPM_BUILD_ROOT
%makeinstall_std
ln -s %_bindir/mkudffs %buildroot/%_bindir/mkfs.udffs
ln -s %_bindir/udffsck %buildroot/%_bindir/fsck.udffs

install -d %buildroot/%_initrddir
install -d %buildroot/%_sysconfdir/sysconfig

bzcat %{SOURCE1} >  %buildroot/%_initrddir/pktcdvd
bzcat %{SOURCE2} >  %buildroot/%_sysconfdir/sysconfig/pktcdvd
bzcat %{SOURCE3} >  doc/pktcdvd.html
bzcat %{SOURCE4} >  doc/pktcdvd-hint.txt

%clean
rm -Rf $RPM_BUILD_ROOT

%post
%_post_service pktcdvd

%preun
%_preun_service pktcdvd

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif


%files
%defattr (- ,root,root)
%doc ChangeLog AUTHORS doc/pktcdvd*
%{_bindir}/*
%attr (0755,root,root) %{_initrddir}/pktcdvd
%config (noreplace) %{_sysconfdir}/sysconfig/pktcdvd
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*

%files -n %{libname}
%defattr (- ,root,root)
%_libdir/*.so.*

%files -n %{develname}
%defattr(-, root, root)
%_libdir/*.so
%_libdir/*.la

%files -n %sdevelname
%defattr(-,root,root)
%{_libdir}/lib*.a

