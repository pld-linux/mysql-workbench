# TODO:
# - something wrong after start:
#   ** Message: WARNING: Could not open module /usr/lib64/mysql-workbench/modules/wb.mysql.import.grt.so (/usr/lib64/mysql-workbench/modules/wb.mysql.import.grt.so: undefined symbol: _ZN19Mysql_sql_parser_feC1Ev)
#   ** Message: WARNING: Could not load wb.mysql.import.grt.so: Cannot open /usr/lib64/mysql-workbench/modules/wb.mysql.import.grt.so
# - runs but not tested at all
# - what with mysql-workbench from mysql-gui-tools.spec?
%define	subver	alpha
Summary:	Extensible modeling tool for MySQL
Summary(pl.UTF-8):	Narzędzie do modelowania baz danych dla MySQL-a
Name:		mysql-workbench
Version:	5.1.4
Release:	0.%{subver}.1
License:	GPL v2
Group:		Applications/Databases
Source0:	ftp://ftp.mysql.com/pub/mysql/download/gui-tools/%{name}-%{version}%{subver}.tar.gz
# Source0-md5:	5cb8543f3263aabf6c57831f8a3b98c9
Patch0:		%{name}-desktop.patch
URL:		http://dev.mysql.com/workbench/
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.3.12
BuildRequires:	ctemplate-devel
BuildRequires:	glib2-devel
BuildRequires:	gtkmm-devel >= 2.4
BuildRequires:	libglade2-devel
BuildRequires:	libgnome-devel >= 2.0
BuildRequires:	libsigc++-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libzip-devel
BuildRequires:	lua51-devel
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL Workbench is a database modeling tool for MySQL. You can use it
to design and create new database schemas, document existing databases
and even perform complex migrations to MySQL.

%description -l pl.UTF-8
MySQL Workbench to narzędzie do modelowania baz danych dla MySQL-a.
Można używać go do projektowania i tworzenia schematów nowych baz
danych, dokumentowania istniejących baz danych, a nawet wykonywania
skomplikowanych migracji do MySQL-a.

%prep
%setup -q -n %{name}-%{version}%{subver}
%patch0 -p1
%{__sed} -i -e 's#/lib/#/%{_lib}/#g' frontend/linux/workbench/%{name}
%{__sed} -i -e 's#!/bin/bash#!/bin/sh#g' frontend/linux/workbench/%{name}

%build
%{__glib_gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} -Wno-deprecated" \
	LUA_LIBS="`pkg-config --libs lua51`" \
	LUA_CFLAGS="`pkg-config --cflags lua51`"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install images/icons/MySQLWorkbench-128.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
mv -f $RPM_BUILD_ROOT%{_desktopdir}/{MySQLWorkbench,%{name}}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-bin
%attr(755,root,root) %{_bindir}/grtshell
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
