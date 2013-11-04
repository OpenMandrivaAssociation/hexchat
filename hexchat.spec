Summary:	A popular and easy to use graphical IRC (chat) client
Name:		hexchat
Version:	2.9.6.1
Release:	1
Group:		Networking/IRC
License:	GPLv2+
URL:		http://www.hexchat.org
Source0:	http://dl.hexchat.net/hexchat/%{name}-%{version}.tar.xz

BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	tcl-devel
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(libsexy)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	openssl-devel
BuildRequires:	desktop-file-utils

%description
HexChat is an easy to use graphical IRC chat client for the X Window System.
It allows you to join multiple IRC channels (chat rooms) at the same time, 
talk publicly, private one-on-one conversations etc. Even file transfers
are possible.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
find -type f -exec chmod a-x {} \;
find -name configure -exec chmod a+x {} \;

%configure2_5x \
		--enable-ipv6 \
        --enable-spell=libsexy \
        --enable-shm

%make

%install
%makeinstall_std

# Add SVG for hicolor
install -D -m644 share/icons/hexchat.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/hexchat.svg

# Get rid of libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} ';'

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
%doc share/doc/*
%dir %{_libdir}/hexchat
%dir %{_libdir}/hexchat/plugins
%{_bindir}/hexchat
%{_libdir}/hexchat/plugins/checksum.so
%{_libdir}/hexchat/plugins/doat.so
%{_libdir}/hexchat/plugins/fishlim.so
%{_libdir}/hexchat/plugins/sysinfo.so
%{_libdir}/hexchat/plugins/perl.so
%{_libdir}/hexchat/plugins/python.so
%{_datadir}/applications/hexchat.desktop
%{_datadir}/icons/hicolor/scalable/apps/hexchat.svg
%{_datadir}/pixmaps/*
%{_datadir}/dbus-1/services/org.hexchat.service.service
%{_mandir}/man1/*.gz
