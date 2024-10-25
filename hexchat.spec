%define _disable_ld_no_undefined 1
%define _disable_lto 1

Summary:	A popular and easy to use graphical IRC (chat) client
Name:		hexchat
Version:	2.16.2
Release:	2
Group:		Networking/IRC
License:	GPLv2+
URL:		https://hexchat.github.io
#Source0:	http://dl.hexchat.net/hexchat/%{name}-%{version}.tar.xz
Source0:	https://github.com/hexchat/hexchat/releases/download/v%{version}/%{name}-%{version}.tar.xz
BuildRequires:	appstream-util
BuildRequires:	bison
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	gnome-common
BuildRequires:  meson
BuildRequires:	perl-ExtUtils-Embed
BuildRequires:	perl-devel
#BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:	pkgconfig(lua)
BuildRequires:  pkgconfig(luajit)
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(libsexy)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:	pkgconfig(openssl)
BuildRequires:  python3dist(cffi)
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

%files -f %{name}.lang
%dir %{_libdir}/hexchat
%dir %{_libdir}/hexchat/plugins
%{_bindir}/%{name}
%{_libdir}/%{name}/plugins/checksum.so
%{_libdir}/%{name}/plugins/lua.so
%{_libdir}/%{name}/plugins/fishlim.so
%{_libdir}/%{name}/plugins/sysinfo.so
%{_libdir}/%{name}/plugins/perl.so
%{_libdir}/%{name}/plugins/python.so
%{_libdir}/%{name}/python/*.py
%{_datadir}/dbus-1/services/org.hexchat.service.service
%{_datadir}/applications/*.desktop
%{_metainfodir}/io.github.Hexchat.appdata.xml
%{_metainfodir}/io.github.Hexchat.Plugin.*.metainfo.xml
%{_iconsdir}/hicolor/*/apps/*.{png,svg}
%{_mandir}/man1/%{name}.1.*

#-----------------------------------------------------------------------

%package devel
Summary:	Development files allowing to build plugins for the HexChat IRC client
Group:		Development/C
Requires:	%{name} = %{EVRD}

%description devel
Development files allowing to build plugins for the HexChat IRC client

%files devel
%{_includedir}/hexchat-plugin.h
%{_libdir}/pkgconfig/hexchat-plugin.pc

#-----------------------------------------------------------------------

%prep
%setup -q

%build
%meson \
	-Dinstall-plugin-metainfo=true
%meson_build

%install
%meson_install

%find_lang %{name}

