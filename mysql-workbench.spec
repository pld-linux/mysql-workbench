# NOTE
# - change history: http://dev.mysql.com/doc/relnotes/workbench/en/
# TODO
# - server administration is broken: sudo locks up (time to time) and it puts
#   EnterPasswordHere begginning of mysqld.conf if you try to manage settings
# - package docs? (use without "-nodocs" tarball)
#
# Conditional build:
%bcond_without	gnome_keyring	# build with gnome-keyring

Summary:	Extensible modeling tool for MySQL
Summary(pl.UTF-8):	Narzędzie do modelowania baz danych dla MySQL-a
Name:		mysql-workbench
Version:	8.0.34
Release:	1
License:	GPL v2
Group:		Applications/Databases
# Source0Download: http://dev.mysql.com/downloads/workbench/
Source0:	https://dev.mysql.com/get/Downloads/MySQLGUITools/%{name}-community-%{version}-src.tar.gz
# Source0-md5:	8718de577ba7242b85388fd06eea9f4c
Source1:	http://www.antlr.org/download/antlr-4.11.1-complete.jar
# Source1-md5:	3a8e221b166f90d13d70f5dd97941353
Source2:	PLD_Linux_(MySQL_Package).xml
Patch0:		pld-profile.patch
Patch1:		log_slow_queries.patch
Patch2:		wrapper-exec.patch
Patch3:		antlr-res.patch
Patch4:		mysql-version.patch
Patch5:		ldconfig.patch
Patch6:		types.patch
Patch7:		stdint.patch
URL:		http://wb.mysql.com/
BuildRequires:	OpenGL-devel
BuildRequires:	antlr4-cpp-runtime-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1.9
BuildRequires:	boost-devel
BuildRequires:	cairo-devel >= 1.5.12
BuildRequires:	cmake >= 2.8
BuildRequires:	ctemplate >= 2.3
BuildRequires:	ctemplate-devel >= 2.3
BuildRequires:	gdal-devel
BuildRequires:	glib2-devel
BuildRequires:	gtkmm3-devel
BuildRequires:	libgnome-keyring-devel
%{?with_gnome_keyring:BuildRequires:	libgnome-keyring-devel}
BuildRequires:	libsecret-devel
BuildRequires:	libsigc++-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libvsqlitepp-devel
BuildRequires:	libxml2-devel
BuildRequires:	libzip-devel
BuildRequires:	lua51-devel
BuildRequires:	mysql-connector-c++-devel >= 1.1.8
BuildRequires:	/usr/bin/mysql_config
BuildRequires:	pcre-cxx-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	rapidjson-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.658
BuildRequires:	sqlite3-devel
BuildRequires:	swig
BuildRequires:	swig-python
BuildRequires:	tinyxml-devel
BuildRequires:	unixODBC-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
Requires:	desktop-file-utils
Requires:	python3-paramiko
Requires:	python3-pexpect
#Requires:	python3-sqlite
Requires:	shared-mime-info
Requires:	xdg-utils
Suggests:	gnome-keyring
Suggests:	mysql-utilities
Suggests:	python3-pyodbc
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

install -d linux-res/bin
cp -p %{SOURCE1} linux-res/bin

# use System provided libraries
%{__rm} -r ext/Aga.Controls

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python3}\1,' -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
	ext/scintilla/gtk/DepGen.py \
	ext/scintilla/qt/ScintillaEdit/WidgetGen.py \
	ext/scintilla/scripts/Dependencies.py \
	ext/scintilla/scripts/FileGenerator.py \
	ext/scintilla/scripts/HFacer.py \
	ext/scintilla/scripts/LexGen.py \
	ext/scintilla/test/gi/filter-scintilla-h.py \
	ext/scintilla/win32/DepGen.py \
	res/scripts/python/mysqlwbmeb.py

%build
install -d build-dir
cd build-dir
%cmake \
	-DUSE_UNIXODBC=ON \
	-DODBC_LIBRARIES="`%{_bindir}/odbc_config --libs`" \
	-DODBC_INCLUDE_DIRS=%{_includedir} \
	-DODBC_DEFINITIONS="`%{_bindir}/odbc_config --cflags`" \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DWB_INSTALL_DIR_EXECUTABLE=%{_libdir}/%{name} \
	-DMySQL_CONFIG_PATH=%{_bindir}/mysql_config \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build-dir install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-community

# deprecated gnome-vfs install
%{__rm} $RPM_BUILD_ROOT%{_datadir}/mime-info/%{name}.mime

%py3_comp $RPM_BUILD_ROOT%{_libdir}/%{name}
%py3_comp $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_mime_database

%files
%defattr(644,root,root,755)
%doc ChangeLog README.md
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-bin
%attr(755,root,root) %{_bindir}/wbcopytables
%attr(755,root,root) %{_bindir}/wbcopytables-bin


%dir %{_datadir}/%{name}
%{_datadir}/%{name}/__pycache__
%attr(755,root,root) %{_datadir}/%{name}/mysqlwbmeb.py
%{_datadir}/%{name}/*.glade
%{_datadir}/%{name}/*.py.txt
%{_datadir}/%{name}/*.css
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
%{_libdir}/%{name}/modules/__pycache__
%{_libdir}/%{name}/modules/*.py
%attr(755,root,root) %{_libdir}/%{name}/modules/*.so*
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so*

# desktop stuff
%{_datadir}/mime/packages/mysql-workbench.xml
%{_iconsdir}/hicolor/*x*/apps/mysql-workbench.png
%{_iconsdir}/hicolor/*x*/mimetypes/*.png
%{_desktopdir}/%{name}.desktop
