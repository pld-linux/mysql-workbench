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
Version:	6.3.5
Release:	3
License:	GPL v2
Group:		Applications/Databases
# Source0Download: http://dev.mysql.com/downloads/workbench/
Source0:	http://cdn.mysql.com/Downloads/MySQLGUITools/%{name}-community-%{version}-src.tar.gz
# Source0-md5:	efe4caf5ccd45e2d6d69778f294aa2c0
Source1:	http://www.antlr3.org/download/antlr-3.4-complete.jar
# Source1-md5:	1b91dea1c7d480b3223f7c8a9aa0e172
Source2:	PLD_Linux_(MySQL_Package).xml
Patch0:		pld-profile.patch
Patch1:		log_slow_queries.patch
Patch2:		bashism.patch
Patch3:		wrapper-exec.patch
Patch4:		antlr-res.patch
Patch5:		mysql-workbench-bug-78668.patch
Patch6:		mysql-workbench-json.patch
Patch7:		gcc6.patch
URL:		http://wb.mysql.com/
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1.9
BuildRequires:	boost-devel
BuildRequires:	cairo-devel >= 1.5.12
BuildRequires:	cmake >= 2.8
BuildRequires:	ctemplate-devel >= 2.3
BuildRequires:	gdal-devel
BuildRequires:	glib2-devel
BuildRequires:	gtkmm-devel >= 2.12
%{?with_system_antlr:BuildRequires:	libantlr3c-devel >= 3.4}
BuildRequires:	libgnome-keyring-devel
%{?with_gnome_keyring:BuildRequires:	libgnome-keyring-devel}
BuildRequires:	libsigc++-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libvsqlitepp-devel
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
BuildRequires:	rpmbuild(macros) >= 1.658
BuildRequires:	sqlite3-devel
BuildRequires:	swig
BuildRequires:	swig-python
BuildRequires:	tinyxml-devel
%{?with_unixodbc:BuildRequires:	unixODBC-devel}
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

%define		specflags			-std=gnu++11

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
%setup -q -n %{name}-community-%{version}-src
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
cp -p '%{SOURCE2}' res/mysql.profiles

%if %{with system_antlr}
rm -r ext/antlr-runtime
%else
install -d linux-res/bin
cp -p %{SOURCE1} linux-res/bin
%endif

# use System provided libraries
#rm -r ext/scintilla
#rm -r ext/HTMLRenderer
#rm -r ext/Aga.Controls

%build
install -d build
cd build
%cmake \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DWB_INSTALL_DIR_EXECUTABLE=%{_libdir}/%{name} \
	-DUSE_UNIXODBC=%{!?with_unixodbc:NO}%{?with_unixodbc:YES} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

# deprecated gnome-vfs install
%{__rm} $RPM_BUILD_ROOT%{_datadir}/mime-info/%{name}.mime

%py_comp $RPM_BUILD_ROOT%{_libdir}/%{name}
%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
# cleaning sshtunnel.py breaks ssh connections
# cleaning the rest fails to import workbench.log
%py_postclean -x sshtunnel.py %{_libdir}/%{name}

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
%attr(755,root,root) %{_bindir}/wbcopytables-bin


%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/sshtunnel.py
%attr(755,root,root) %{_datadir}/%{name}/mysqlwbmeb.py
%{_datadir}/%{name}/*.glade
%{_datadir}/%{name}/*.py.txt
%{_datadir}/%{name}/*.py[co]
%{_datadir}/%{name}/*.rc
%{_datadir}/%{name}/*.vbs
%{_datadir}/%{name}/data
%{_datadir}/%{name}/extras
%{_datadir}/%{name}/grt
%{_datadir}/%{name}/images
%{_datadir}/%{name}/libraries
%{_datadir}/%{name}/modules
%{_datadir}/%{name}/mysql.profiles
%{_datadir}/%{name}/script_templates
%{_datadir}/%{name}/snippets
%{_datadir}/%{name}/sys

%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.py*
%attr(755,root,root) %{_libdir}/%{name}/modules/*.so*
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so*

# desktop stuff
%{_datadir}/mime/packages/mysql-workbench.xml
%{_iconsdir}/hicolor/*x*/apps/mysql-workbench.png
%{_iconsdir}/hicolor/*x*/mimetypes/*.png
%{_desktopdir}/%{name}.desktop
