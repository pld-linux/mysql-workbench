# NOTE
# - change history: http://dev.mysql.com/doc/workbench/en/wb-change-history.html
# TODO
# - server administration is broken: sudo locks up (time to time) and it puts
#   EnterPasswordHere begginning of mysqld.conf if you try to manage settings
Summary:	Extensible modeling tool for MySQL
Summary(pl.UTF-8):	Narzędzie do modelowania baz danych dla MySQL-a
Name:		mysql-workbench
Version:	5.2.40
Release:	1
License:	GPL v2
Group:		Applications/Databases
Source0:	ftp://ftp.mirrorservice.org/sites/ftp.mysql.com/Downloads/MySQLGUITools/%{name}-gpl-%{version}-src.tar.gz
# Source0-md5:	ac5c2058cd39c796a1c7bed2647f74b6
Source1:	PLD_Linux_(MySQL_Package).xml
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-python_libs.patch
Patch2:		%{name}-posix.patch
Patch3:		automake.patch
Patch5:		pld-profile.patch
Patch6:		get_local_ip_list.patch
Patch7:		log_slow_queries.patch
Patch8:		bashism.patch
Patch9:		system-cppconn.patch
Patch10:	avoid-version.patch
Patch11:	wrapper-exec.patch
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
BuildRequires:	mysql-connector-c++-devel >= 1.1.0-0.bzr916
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sqlite3-devel
Requires:	desktop-file-utils
Requires:	python-paramiko
Requires:	python-pexpect
Requires:	python-sqlite
Requires:	shared-mime-info
Requires:	xdg-utils
Suggests:	gnome-keyring
Suggests:	mysql-utilities
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
rm -r ext/python/pexpect
rm -r ext/cppconn
#rm -r ext/tinyxml
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
cp -p '%{SOURCE1}' res/mysql.profiles

%build
%{__glib_gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-dependency-tracking \
	--enable-readline \
	CFLAGS="%{rpmcppflags} %{rpmcflags} -Wno-deprecated" \
	LUA_LIBS="$(pkg-config --libs lua51)" \
	LUA_CFLAGS="$(pkg-config --cflags lua51)"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# clear mimeinfodata_DATA because don't want deprecated gnome-vfs install
%{__make} install \
	doc_DATA= \
	mimeinfodata_DATA= \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir}/%{name} -name '*.la'  | xargs rm -v

%py_comp $RPM_BUILD_ROOT%{_libdir}/%{name}
%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
# cleaning .py breaks ssh connections
#%%py_postclean %{_libdir}/%{name} %{_datadir}/%{name}

install -d $RPM_BUILD_ROOT%{_pixmapsdir}
cp -p images/icons/MySQLWorkbench-128.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

mv $RPM_BUILD_ROOT%{_desktopdir}/{MySQLWorkbench,%{name}}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_mime_database

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-bin
%{_datadir}/%{name}
%{_datadir}/mime/packages/mysql-workbench.xml
%{_iconsdir}/hicolor/*x*/apps/mysql-workbench.png
%{_iconsdir}/hicolor/*x*/mimetypes/*.png
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png

%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.py*
%{_libdir}/%{name}/modules/*.lua
%attr(755,root,root) %{_libdir}/%{name}/modules/*.so*
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so*
