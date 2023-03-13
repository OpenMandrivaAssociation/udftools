Summary:	UDF filesystem tools
Name:		udftools
Epoch:		1
Version:	2.3
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		https://github.com/pali/udftools
Source0:	https://github.com/pali/udftools/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(udev)
Provides:	udf = %{EVRD}
Obsoletes:	udf <= 1.0

%description -n udftools
These are tools for UDF file systems as used, e.g.,
on DVD-RAM, DVD+RW, CD-RW. They are also used for
managing Packet-CD/DVD devices and media.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -rf  %{buildroot}%{_docdir}/%{name}

%files
%doc ChangeLog AUTHORS
%{_udevrulesdir}/80-pktsetup.rules
%{_bindir}/*
%doc %{_mandir}/man1/*.1*
%doc %{_mandir}/man8/*.8*
