%define name_plugin	%{name}_plugin

%define cvs	20071220
%if %cvs
%define release	%mkrel 0.%cvs.5
%else
%define release %mkrel 1
%endif

%define pilot_link_version 0.12.0

Summary:	Palm pilot desktop for Linux
Name:		jpilot
Version:	0.99.10
Release:	%{release}
License:	GPLv2
Group:		Communications
URL:		http://www.jpilot.org/
%if %cvs
Source0:	%{name}-%{cvs}.tar.lzma
%else
Source0:	http://jpilot.org/%{name}-%{version}.tar.bz2
%endif
Patch1:		jpilot-0.99.4-usbinfo.patch
Patch2:		jpilot-0.99.1u-plugins-improvement.patch
Patch3:		jpilot-0.99.10-lib64.patch
Patch4:		jpilot-libtool_fixes.diff
Patch5:		jpilot-libdir_fix.diff
Patch6:		jpilot-wformat.patch
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
%if %cvs
BuildRequires:	gettext-devel
BuildRequires:	intltool
%endif
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

%if %cvs
%setup -q -n %{name}
%else
%setup -q
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
sed -i -e 's,the Palm Pilot,Palm PDAs,g' %{name}.desktop
sed -i -e 's,Exec=%{name},Exec=%{_bindir}/%{name},g' %{name}.desktop
sed -i -e 's,%{name}.xpm,%{name},g' %{name}.desktop

%build
%if %cvs
NOCONFIGURE=1 ./autogen.sh
%endif
%if %_lib == lib64
  %define conf_args enable_libsuffix=64
%else 
  %define conf_args ""
%endif
%configure2_5x %conf_args
%make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_mandir}/man1,%{_bindir}}

%makeinstall libdir=%{buildroot}/%{_libdir}/%{name}/plugins

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
