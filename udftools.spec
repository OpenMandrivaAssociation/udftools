%define beta	b3
%define tarver	%{version}%{beta}cvs20040419
%define mdkrel	14


%if %beta
%define release 0.%{beta}.%{mdkrel}
%else
%define release %{mdkrel}
%endif

%define major 1
%define libname %mklibname udftools %{major}
%define develname %mklibname -d udftools
%define sdevelname %mklibname -d -s udftools


Name:		udftools
Version:	1.0.0
Release:	%{release}
Epoch:		1
License:	GPLv2+
Group:		System/Kernel and hardware
Provides:	udf
Obsoletes:	udf
Autoreqprov:	off
Summary:	UDF filesystem tools
Source0:	%{name}-%{tarver}.tar.bz2
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
Patch7:		udftools-include.patch
URL:		http://sourceforge.net/projects/linux-udf/
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
Provides:	%{libname} = %{EVRD}
Provides:	libudftools = %{EVRD}

%description -n %{libname}
This package contains the libraries meeded by %name.


%package -n %{develname}
Summary:	Devel files from %name
Group:		Development/C
Requires:	%{libname} = %version-%release
Provides:	libudftools-devel = %{EVRD}
Provides:	%name-devel = %{EVRD}
Provides:	%{libname}-devel = %{EVRD}
Obsoletes:	%mklibname -d udftools 1

%description -n %{develname}
This is the libraries, include files and other resources you can use
to incorporate %name into applications.

%package -n %sdevelname
Summary:	Static Library for developing applications with %name
Group:		Development/C
Requires:	%develname = %epoch:%version-%release
Provides:	udftools-static-devel = %{EVRD}
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
%patch7 -p0
perl -pi -e 's! udfct/Makefile! udfct/Makefile cdmrw/Makefile!' configure.in
perl -pi -e 's! udfct! udfct cdmrw!' Makefile.am

%build
%define _disable_ld_no_undefined 1
autoreconf --force --install
%configure2_5x --enable-shared
%make

%install
%makeinstall_std
ln -s %_bindir/mkudffs %buildroot/%_bindir/mkfs.udffs
ln -s %_bindir/udffsck %buildroot/%_bindir/fsck.udffs

install -d %buildroot/%_initrddir
install -d %buildroot/%_sysconfdir/sysconfig

bzcat %{SOURCE1} >  %buildroot/%_initrddir/pktcdvd
bzcat %{SOURCE2} >  %buildroot/%_sysconfdir/sysconfig/pktcdvd
bzcat %{SOURCE3} >  doc/pktcdvd.html
bzcat %{SOURCE4} >  doc/pktcdvd-hint.txt

%post
%_post_service pktcdvd

%preun
%_preun_service pktcdvd


%files
%doc ChangeLog AUTHORS doc/pktcdvd*
%{_bindir}/*
%attr (0755,root,root) %{_initrddir}/pktcdvd
%config (noreplace) %{_sysconfdir}/sysconfig/pktcdvd
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*

%files -n %{libname}
%_libdir/*.so.*

%files -n %{develname}
%_libdir/*.so

%files -n %sdevelname
%{_libdir}/lib*.a



%changelog
* Sat Aug 23 2008 Funda Wang <fundawang@mandriva.org> 1:1.0.0-0.b3.13mdv2009.0
+ Revision: 275403
- more gcc 4.3 patch
- add gcc 4.3 patch from suse
- add patch from suse
- bzunzip patches

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - rebuild
    - fix summary-ended-with-dot

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Dec 20 2007 Thierry Vignaud <tvignaud@mandriva.com> 1:1.0.0-0.b3.10mdv2008.1
+ Revision: 135779
- fix autoconf path
- kill re-definition of %%buildroot on Pixel's request
- do not hardcode man pages extension
- import udftools


* Fri Oct 28 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.0.0-0.b3.10mdk
- Fix BuildRequires

* Fri Oct 28 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.0.0-0.b3.9mdk
- patch 5 : Fix build with gcc4
- Fix PreReq
- %%mkrel

* Fri Nov 19 2004 Marcel Pol <mpol@mandrake.org> 1.0.0-0.b3.8mdk
- buildrequires readline-devel
- prerequires rpm-helper
- autoconf2.5 is default now

* Fri Oct 08 2004 Marcel Pol <mpol@mandrake.org> 1.0.0-0.b3.7mdk
- from couriousous <couriousous at zarb.org>
  update initscript and sysconfig file (bug #12018)

* Fri Sep 10 2004 couriousous <couriousous@zarb.org> 1.0.0-0.b3.6mdk
- Patch4 for 2.6.8.1 kernel

* Tue Jul 27 2004 svetljo<svetljo@gmx.de> 2.3.4-4mdk
- rebuild

* Thu Jun 13 2004 Svetoslav Slavtchev <svetljo@gmx.de> 1.0.0b3-4mdk
- drop club stuff
- update email

* Mon Apr 26 2004 Svetoslav Slavtchev <galia@st-peter.stw.uni-erlangen.de> 1.0.0b3-3mdk
- fix config file path
- install the other doc too

* Tue Apr 20 2004 Svetoslav Slavtchev <galia@st-peter.stw.uni-erlangen.de> 1.0.0b3-2mdk
- update to cvs 20040419
  ( fixes compilation of wrudf & udffsck )
- add init scripts
- add mkfs.udffs & fsck.udffs symlinks
- add some docs from the net
  ( need mdk-fication)
- add missing changelog

* Fri Apr 02 2004 Svetoslav Slavtchev <galia@st-peter.stw.uni-erlangen.de> 1.0.0b3-1mdk
- 1.0.0-b3 final
- add cdmrw tool

* Fri Aug 29 2003 Marcel Pol <mpol@gmx.net> 1.0.0-0.b3.20030825.1mdk
- beta is part of release tag, not version
- make sure to use autoconf-2.5 and automake-1.7
- other small changes in specfile

* Tue Aug 26 2003 Svetoslav Slavtchev <galia@st-peter.stw.uni-erlangen.de> 1.0.0b3-0.20030825.1mdk
- initial release

