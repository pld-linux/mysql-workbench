Summary:	Extensible modeling tool for MySQL
Summary(pl.UTF-8):	Narzędzie do modelowania baz danych dla MySQL-a
Name:		mysql-workbench
Version:	5.2.33
Release:	5
License:	GPL v2
Group:		Applications/Databases
Source0:	ftp://ftp.mirrorservice.org/sites/ftp.mysql.com/Downloads/MySQLGUITools/%{name}-gpl-%{version}b-src.tar.gz
# Source0-md5:	850e081eeaea87a88c408483817e4b1f
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-python_libs.patch
Patch2:		%{name}-replace_gnome_url_show_by_xdg-open.patch
URL:		http://wb.mysql.com/
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel
BuildRequires:	cairo-devel >= 1.3.12
BuildRequires:	ctemplate-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	gtkmm-devel >= 2.4
BuildRequires:	libglade2-devel
BuildRequires:	libgnome-devel >= 2.0
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libsigc++-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libzip-devel
BuildRequires:	lua51-devel
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sqlite3-devel
Requires:	python-paramiko
Requires:	python-pexpect
Requires:	python-sqlite
# Patch2 requires xdg-utils
Requires:	xdg-utils
Suggests:	gnome-keyring
Suggests:	sudo
Obsoletes:	mysql-administrator
Obsoletes:	mysql-gui-tools
Obsoletes:	mysql-query-browser
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# too broken
%define		no_install_post_check_so	1

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
%setup -q -n %{name}-gpl-%{version}-src
%undos MySQLWorkbench.desktop.in
# we use System provided libraries
rm -rf ext/boost
rm -rf ext/curl
rm -rf ext/libsigc++
rm -rf ext/yassl
# rm -rf ext/cppconn
# rm -rf ext/ctemplate
# rm -rf library/tinyxml
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__glib_gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-readline \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -Wno-deprecated" \
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
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
