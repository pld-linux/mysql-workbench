Summary:	A database modeling tool for MySQL
Name:		mysql-workbench
Version:	1.0.5
Release:	0.beta.1
License:	GPL
Group:		Applications/Databases
Source0:	ftp://ftp.mysql.com/pub/mysql/download/%{name}-%{version}beta.tar.gz
# Source0-md5:	a3f40d5bb5075775fe5c35024048d396
URL:		http://forge.mysql.com/wiki/index.php/MySQL_Workbench
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtkhtml-devel >= 3.6.0
BuildRequires:	gtkmm-devel >= 2.4.0
BuildRequires:	libglade2-devel >= 1:2.0.0
BuildRequires:	libgtkhtml-devel
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL Workbench is a database modeling tool for MySQL. You can use it
to design and create new database schemas, document existing databases
and even perform complex migrations to MySQL.

%prep
%setup -q -n %{name}-%{version}beta

%build
export PKG_CONFIG=pkg-config
# first we have to build the common libs
cd mysql-gui-common
install /usr/share/automake/config.* .
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gtkhtml=libgtkhtml-3.8 \
	--with-commondirname=workbench
%{__make}

# then the app itself
cd ../%{name}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gtkhtml=libgtkhtml-3.8 \
	--with-commondirname=workbench
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C mysql-gui-common install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C %{name} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/mysql-gui/doc/workbench
cp -a mysql-workbench/doc/* $RPM_BUILD_ROOT%{_datadir}/mysql-gui/doc/workbench

%find_lang mysql-gui-common
%find_lang %{name}
cat mysql-gui-common.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql-workbench
%attr(755,root,root) %{_bindir}/mysql-workbench-bin
%{_desktopdir}/*.desktop
%{_datadir}/mysql-gui/*.png

%dir %{_datadir}/mysql-gui
%dir %{_datadir}/mysql-gui/workbench
%{_datadir}/mysql-gui/workbench/*

# duplicate with mysql-administrator?
%dir %{_datadir}/mysql-gui/doc
%dir %{_datadir}/mysql-gui/doc/workbench
%{_datadir}/mysql-gui/doc/workbench/*
