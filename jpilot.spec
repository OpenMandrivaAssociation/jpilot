%define name_plugin	%{name}_plugin

%define pilot_link_version 0.12.0

Summary:	Palm pilot desktop for Linux
Name:		jpilot
Version:	1.6.2
Release:	%mkrel 3
License:	GPLv2
Group:		Communications
URL:		http://www.jpilot.org/
Source0:	http://jpilot.org/%{name}-%{version}.tar.gz
Patch1:		jpilot-1.6.2-usbinfo.patch
Patch2:		jpilot-0.99.1u-plugins-improvement.patch
Patch4:		jpilot-1.6.2-linkage.patch
Patch5:		jpilot-1.6.2-libdir-fix.patch
Patch6:		jpilot-1.6.2-fix-str-fmt.patch
Patch7:		jpilot-1.6.2-fix-desktop.patch
Requires:	pilot-link >= %{pilot_link_version}
Requires:	jpilot-expense
Requires:	jpilot-keyring
Requires:	jpilot-synctime
BuildRequires:	imagemagick
BuildRequires:  desktop-file-utils
BuildRequires:	gtk2-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pilot-link-devel >= %{pilot_link_version}
BuildRequires:	readline-devel
BuildRequires:	perl-XML-Parser
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

%package	expense
Summary:	The expense plugin for jpilot
Group:		Communications
Obsoletes:	%{mklibname jpilot_plugin 0} < %{version}-%{release}

%description	expense
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

This package contains the expense plugin for jpilot.

%package	keyring
Summary:	The keyring plugin for jpilot
Group:		Communications
Obsoletes:	%{mklibname jpilot_plugin 0} < %{version}-%{release}

%description	keyring
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

This package contains the keyring plugin for jpilot.

%package	synctime
Summary:	The synctime plugin for jpilot
Group:		Communications
Obsoletes:	%{mklibname jpilot_plugin 0} < %{version}-%{release}

%description	synctime
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

This package contains the synctime plugin for jpilot.

%package	devel
Summary:	Header file needed for jpilot plugin development
Group:		Development/C
Provides:	%{name_plugin}-devel = %{version}
Obsoletes:	%{mklibname jpilot_plugin 0 -d} < %{version}-%{release}
Obsoletes:	%{mklibname jpilot_plugin -d} < %{version}-%{release}

%description	devel
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that 
3Com distributes for a well known rampant legacy operating system.

The header files required for plugin development.

%prep
%setup -q
%patch1 -p1 -b .usbinfo
%patch2 -p1 -b .plugins
%patch4 -p0 -b .linkage
%patch5 -p0 -b .libdir
%patch6 -p0 -b .str
%patch7 -p0 -b .desktop

%build
export ABILIB="%_lib"
%configure2_5x
%make

%install
rm -rf %{buildroot}
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
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %{name}

# cleanup
rm -f %{buildroot}/%{_libdir}/%{name}/plugins/*.la

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun 
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog README TODO
%doc docs/manual.html docs/jpilot-*.png docs/jpilot-*.jpg
%{_bindir}/*
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*
%{_mandir}/man1/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins

%files expense
%defattr(-,root,root)
%{_libdir}/%{name}/plugins/libexpense.so

%files keyring
%defattr(-,root,root)
%{_libdir}/%{name}/plugins/libkeyring.so

%files synctime
%defattr(-,root,root)
%{_libdir}/%{name}/plugins/libsynctime.so

%files devel
%defattr(-,root,root)
%doc docs/plugin.html
%{_includedir}/*.h
