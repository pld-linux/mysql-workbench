# TODO:
# - something wrong after start:
#   ** Message: WARNING: Could not open module /usr/lib64/mysql-workbench/modules/wb.mysql.import.grt.so (/usr/lib64/mysql-workbench/modules/wb.mysql.import.grt.so: undefined symbol: _ZN19Mysql_sql_parser_feC1Ev)
#   ** Message: WARNING: Could not load wb.mysql.import.grt.so: Cannot open /usr/lib64/mysql-workbench/modules/wb.mysql.import.grt.so
# - runs but not tested at all
# - what with mysql-workbench from mysql-gui-tools.spec?
# - doesn't build, -Wl,--as-needed problem,
#   with %%define filterout_ld -Wl,--as-needed builds fine

Summary:	Extensible modeling tool for MySQL
Summary(pl.UTF-8):	Narzędzie do modelowania baz danych dla MySQL-a
Name:		mysql-workbench
Version:	5.1.17
Release:	1
License:	GPL v2
Group:		Applications/Databases
Source0:	ftp://ftp.mirrorservice.org/sites/ftp.mysql.com/Downloads/MySQLGUITools/%{name}-oss-%{version}.tar.gz
# Source0-md5:	2c7e1adfd100d23dc47295037e0bec68
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-build.patch
URL:		http://wb.mysql.com/
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel
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
BuildRequires:	readline-devel
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# FIXME: fix linking of m/usr/lib{,64}/mysql-workbench/plugins/*.so* modules and then drop this
%define		filterout_ld	-Wl,--as-needed

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
%setup -q -n %{name}-oss-%{version}
%undos MySQLWorkbench.desktop.in
rm -rf ext/boost
%patch0 -p1
%patch1 -p1

%build
%{__glib_gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-readline \
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
