# NOTE
# - change history: http://dev.mysql.com/doc/relnotes/workbench/en/
# TODO
# - server administration is broken: sudo locks up (time to time) and it puts
#   EnterPasswordHere begginning of mysqld.conf if you try to manage settings
# - package docs? (use without "-nodocs" tarball)
#
# Conditional build:
%bcond_without	gnome_keyring	# build with gnome-keyring
%bcond_without	unixodbc		# Use unixODBC instead of iODBC
%bcond_with	system_antlr	# Use system antlr (All known publicly available versions of Antlr3C are buggy)

Summary:	Extensible modeling tool for MySQL
Summary(pl.UTF-8):	Narzędzie do modelowania baz danych dla MySQL-a
Name:		mysql-workbench
Version:	6.1.4
Release:	0.3
License:	GPL v2
Group:		Applications/Databases
Source0:	http://cdn.mysql.com/Downloads/MySQLGUITools/%{name}-community-%{version}-nodocs-src.tar.gz
# Source0-md5:	c0aa6043c75a8fb810cc1ef60cc916a4
Source1:	PLD_Linux_(MySQL_Package).xml
Patch5:		pld-profile.patch
Patch7:		log_slow_queries.patch
Patch8:		bashism.patch
Patch11:	wrapper-exec.patch
URL:		http://wb.mysql.com/
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1.9
BuildRequires:	boost-devel
BuildRequires:	cairo-devel >= 1.5.12
BuildRequires:	cmake >= 2.8
BuildRequires:	ctemplate-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	gtkmm-devel >= 2.12
BuildRequires:	libantlr3c-devel >= 3.4
BuildRequires:	libglade2-devel
#BuildRequires:	libgnome-devel >= 2.0
BuildRequires:	libgnome-keyring-devel
%{?with_gnome_keyring:BuildRequires:	libgnome-keyring-devel}
BuildRequires:	libsigc++-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel
BuildRequires:	libzip-devel
BuildRequires:	lua51-devel
BuildRequires:	mysql-connector-c++-devel >= 1.1.0-0.bzr916
BuildRequires:	mysql-devel
BuildRequires:	pcre-cxx-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sqlite3-devel
BuildRequires:	swig
BuildRequires:	tinyxml-devel
%{?with_unixodbc:BuildRequires:	unixODBC-devel}
BuildRequires:	libvsqlitepp-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
Requires:	desktop-file-utils
Requires:	python-paramiko
Requires:	python-pexpect
Requires:	python-sqlite
Requires:	shared-mime-info
Requires:	xdg-utils
Suggests:	gnome-keyring
Suggests:	mysql-utilities
Suggests:	python-pyodbc
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
%setup -q -n %{name}-community-%{version}-nodocs-src
%patch5 -p1
%patch7 -p1
%patch8 -p1
%patch11 -p1
cp -p '%{SOURCE1}' res/mysql.profiles

# use System provided libraries
%{?with_system_antlr:rm -r ext/antlr-runtime}
#rm -r ext/scintilla
#rm -r ext/HTMLRenderer
#rm -r ext/Aga.Controls

%build
%cmake . \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DWB_INSTALL_DIR_EXECUTABLE=%{_libdir}/%{name} \
	-DUSE_UNIXODBC=%{!?with_unixodbc:NO}%{?with_unixodbc:YES}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

# deprecated gnome-vfs install
%{__rm} $RPM_BUILD_ROOT%{_datadir}/mime-info/%{name}.mime

%py_comp $RPM_BUILD_ROOT%{_libdir}/%{name}
%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
# cleaning .py breaks ssh connections
%py_postclean %{_libdir}/%{name} %{_datadir}/%{name}

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
%attr(755,root,root) %{_bindir}/wbcopytables

%{_datadir}/%{name}
%{_datadir}/mime/packages/mysql-workbench.xml
%{_iconsdir}/hicolor/*x*/apps/mysql-workbench.png
%{_iconsdir}/hicolor/*x*/mimetypes/*.png
%{_desktopdir}/%{name}.desktop

%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.py*
%attr(755,root,root) %{_libdir}/%{name}/modules/*.so
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
