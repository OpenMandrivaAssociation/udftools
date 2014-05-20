%define beta b3
%define tarver %{version}%{beta}cvs20040419
%define mdkrel 15

%if %{beta}
%define release 0.%{beta}.%{mdkrel}
%else
%define release %{mdkrel}
%endif

%define major 1
%define libname %mklibname udffs %{major}
%define devname %mklibname udffs -d

Summary:	UDF filesystem tools
Name:		udftools
Version:	1.0.0
Release:	%{release}
Epoch:		1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://sourceforge.net/projects/linux-udf/
Source0:	%{name}-%{tarver}.tar.bz2
Source1:	pktcdvd.init.d.bz2
Source2:	pktcdvd.sysconfig.bz2
Source3:	pktcdvd.html.bz2
Source4:	pktcdvd-hint.txt.bz2
Patch2:		udftools-disable_broken.patch
Patch3:		udftools-1.0.0b3cvs_add_cdmrw.patch
Patch4:		udftools-1.0.0b3-kernel-2.6.8.1.patch
Patch5:		udftools-1.0.0-gcc4.patch
Patch6:		udftools-open.patch
Patch7:		udftools-include.patch
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Provides:	udf = %{EVRD}

%description -n udftools
These are tools for UDF file systems as used, e.g., on DVD-RAM, DVD+RW, CD-RW.
They are also used for managing Packet-CD/DVD devices and media.

%files
%doc ChangeLog AUTHORS doc/pktcdvd*
%{_bindir}/*
%attr (0755,root,root) %{_initrddir}/pktcdvd
%config (noreplace) %{_sysconfdir}/sysconfig/pktcdvd
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*

%post
%_post_service pktcdvd

%preun
%_preun_service pktcdvd

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
Obsoletes:	%{_lib}udftools1 < 1:1.0.0-0.b3.15
Conflicts:	%{_lib}udftools1 < 1:1.0.0-0.b3.15

%description -n %{libname}
This package contains the libraries needed by %{name}.

%files -n %{libname}
%{_libdir}/libudffs.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Devel files from %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}udftools-devel < 1:1.0.0-0.b3.15
Conflicts:	%{_lib}udftools-devel < 1:1.0.0-0.b3.15
Obsoletes:	%{_lib}udftools-static-devel < 1:1.0.0-0.b3.15

%description -n %{devname}
This is the libraries, include files and other resources you can use
to incorporate %{name} into applications.

%files -n %{devname}
%{_libdir}/libudffs.so

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}
%patch3 -p1
%patch4 -p1 -b .kernel-2.6.8.1
%patch5 -p1 -b .gcc4
%patch6 -p0
%patch7 -p0
perl -pi -e 's! udfct/Makefile! udfct/Makefile cdmrw/Makefile!' configure.in
perl -pi -e 's! udfct! udfct cdmrw!' Makefile.am

%build
%define _disable_ld_no_undefined 1
autoreconf -fi
%configure2_5x \
	--enable-shared \
	--disable-static
%make

%install
%makeinstall_std
ln -s %{_bindir}/mkudffs %{buildroot}%{_bindir}/mkfs.udffs
ln -s %{_bindir}/udffsck %{buildroot}%{_bindir}/fsck.udffs

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig

bzcat %{SOURCE1} > %{buildroot}%{_initrddir}/pktcdvd
bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/sysconfig/pktcdvd
bzcat %{SOURCE3} > doc/pktcdvd.html
bzcat %{SOURCE4} > doc/pktcdvd-hint.txt
