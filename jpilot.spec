%define _disable_ld_no_undefined 1

%define name_plugin %{name}_plugin
%define pilot_link_version 0.12.5

Summary:	Palm pilot desktop for Linux
Name:		jpilot
Version:	1.8.2
Release:	5
License:	GPLv2+
Group:		Communications
Url:		https://www.jpilot.org/
Source0:	http://jpilot.org/%{name}-%{version}.tar.gz
Patch2:		jpilot-0.99.1u-plugins-improvement.patch
Patch4:		jpilot-1.8.0-linkage.patch
Patch7:		jpilot-1.6.2-fix-desktop.patch

BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	perl-XML-Parser
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(pilot-link) >= %{pilot_link_version}
Requires:	jpilot-expense
Requires:	jpilot-keyring
Requires:	jpilot-synctime
Requires:	pilot-link >= %{pilot_link_version}

%description
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog README TODO
%doc docs/manual.html docs/jpilot-*.png docs/jpilot-*.jpg
%{_bindir}/*
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*
%{_mandir}/man1/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins

#----------------------------------------------------------------------------

%package expense
Summary:	The expense plugin for jpilot
Group:		Communications

%description expense
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

This package contains the expense plugin for jpilot.

%files expense
%{_libdir}/%{name}/plugins/libexpense.so

#----------------------------------------------------------------------------

%package keyring
Summary:	The keyring plugin for jpilot
Group:		Communications

%description keyring
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

This package contains the keyring plugin for jpilot.

%files keyring
%{_libdir}/%{name}/plugins/libkeyring.so

#----------------------------------------------------------------------------

%package synctime
Summary:	The synctime plugin for jpilot
Group:		Communications

%description synctime
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

This package contains the synctime plugin for jpilot.

%files synctime
%{_libdir}/%{name}/plugins/libsynctime.so

#----------------------------------------------------------------------------

%package devel
Summary:	Header file needed for jpilot plugin development
Group:		Development/C
Provides:	%{name_plugin}-devel = %{EVRD}

%description devel
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that 
3Com distributes for a well known rampant legacy operating system.

The header files required for plugin development.

%files devel
%doc docs/plugin.html
%{_includedir}/*.h

#----------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

%build
export ABILIB="%{_lib}"
%configure2_5x
%make

%install
%makeinstall_std

# copy empty/*.pdb in %{_datadir}/jpilot/
mkdir -p %{buildroot}%{_datadir}/jpilot
cp empty/*.pdb %{buildroot}%{_datadir}/jpilot/

# copy jpilotrc.* in %{_datadir}/jpilot/
cp jpilotrc.* %{buildroot}%{_datadir}/jpilot/

# clean documentation done by makefile itself.
rm -rf %{buildroot}/usr/doc

mkdir -p %{buildroot}/%{_includedir}
install -m 644 {libplugin,prefs}.h %{buildroot}%{_includedir}/

# use builtin icons and ImageMagick to do the conversion.
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -resize 16x16 icons/jpilot-icon1.xpm %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -resize 32x32 icons/jpilot-icon1.xpm %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -resize 48x48 icons/jpilot-icon1.xpm %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

desktop-file-install --vendor="" \
	--remove-key="Encoding" \
	--remove-category="Application" \
	--add-category="GTK" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%find_lang %{name}

