Summary:	A popular and easy to use graphical IRC (chat) client
Name:		hexchat
Version:	2.14.3
Release:	1
Group:		Networking/IRC
License:	GPLv2+
URL:		https://hexchat.github.io
Source0:	http://dl.hexchat.net/hexchat/%{name}-%{version}.tar.xz
BuildRequires:  meson
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	perl-ExtUtils-Embed
BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	tcl-devel
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(libsexy)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(python)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  pkgconfig(luajit)
BuildRequires:	openssl-devel
BuildRequires:	desktop-file-utils
BuildRequires:	autoconf-archive

# This is a fork of abandoned xchat -- so let's give
# users what they're looking for.
%rename xchat

%description
HexChat is an easy to use graphical IRC chat client for the X Window System.
It allows you to join multiple IRC channels (chat rooms) at the same time, 
talk publicly, private one-on-one conversations etc. Even file transfers
are possible.

%package devel
Summary:	Development files allowing to build plugins for the HexChat IRC client
Group:		Development/C
Requires:	%{name} = %{EVRD}

%description devel
Development files allowing to build plugins for the HexChat IRC client

%prep
%setup -q
# fix python3.8 linking
sed -i -e '/with-python/s,python3,python3-embed,g' meson_options.txt

%build
export CC=gcc
export CXX=g++
%meson
%meson_build

%install
%meson_install

# Add SVG for hicolor
install -D -m644 data/icons/hexchat.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/hexchat.svg

# Drop deprecated TCL plugin
find %{buildroot} -name 'tcl.so' -exec rm -f {} ';'

# Remove unused schema
rm -f %{buildroot}%{_sysconfdir}/gconf/schemas/apps_hexchat_url_handler.schemas

# Fix opening irc:// links by adding mimetype and editing exec
desktop-file-install \
    --add-mime-type='x-scheme-handler/irc;x-scheme-handler/ircs' \
    --remove-key=Exec \
    --dir=%{buildroot}%{_datadir}/applications/ \
    %{buildroot}%{_datadir}/applications/hexchat.desktop

# Workaround for EL's version of desktop-file-install
echo Exec="sh -c \"hexchat --existing --url %U || exec hexchat\"">>%{buildroot}%{_datadir}/applications/hexchat.desktop

%find_lang %{name}

%files -f %{name}.lang
%dir %{_libdir}/hexchat
%dir %{_libdir}/hexchat/plugins
%{_bindir}/hexchat
%{_libdir}/hexchat/plugins/checksum.so
%{_libdir}/hexchat/plugins/lua.so
%{_libdir}/hexchat/plugins/fishlim.so
%{_libdir}/hexchat/plugins/sysinfo.so
%{_libdir}/hexchat/plugins/perl.so
%{_libdir}/hexchat/plugins/python.so
%{_datadir}/applications/hexchat.desktop
%{_iconsdir}/hicolor/*/apps/*.*g
%{_datadir}/dbus-1/services/org.hexchat.service.service
%{_datadir}/appdata/hexchat.appdata.xml
%{_mandir}/man1/%{name}.1.*

%files devel
%{_includedir}/hexchat-plugin.h
%{_libdir}/pkgconfig/hexchat-plugin.pc
