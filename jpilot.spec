%define name_plugin	%{name}_plugin

%define major		0
%define libname		%mklibname %{name_plugin} %{major}
%define develname	%mklibname %{name_plugin} -d

%define cvs	20071220
%if %cvs
%define release	%mkrel 0.%cvs.1
%else
%define release %mkrel 1
%endif

%define pilot_link_version 0.12.0

Name:		jpilot
Summary:	Palm pilot desktop for Linux
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
Requires:	pilot-link >= %{pilot_link_version}
Requires:	%{libname} = %{version}
BuildRequires:	ImageMagick
BuildRequires:	chrpath
BuildRequires:  desktop-file-utils
BuildRequires:	gtk2-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pilot-link-devel >= %{pilot_link_version}
BuildRequires:	readline-devel
BuildRequires:	perl-XML-Parser
%if %cvs
BuildRequires:	gettext-devel
%endif

%description
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

%package -n	%{libname}
Summary:	Shared libraries for jpilot
Group:		Communications

%description -n	%{libname}
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that
3Com distributes for a well known rampant legacy operating system.

The shared libraries required for jpilot.

%package -n	%{develname}
Summary:	Library and header file needed for jpilot plugin development
Group:		Communications
Requires:	%{libname} = %{version}
Provides:	%{name_plugin}-devel = %{version}
Obsoletes:	%{mklibname jpilot_plugin 0 -d} < %{version}-%{release}

%description -n	%{develname}
J-Pilot is a desktop organizer application for Palm PDAs that runs
under Linux and UNIX.  It is similar in functionality to the one that 
3Com distributes for a well known rampant legacy operating system.

The library and header files required for plugin development.

%prep
%if %cvs
%setup -q -n %{name}
%else
%setup -q
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
sed -i -e 's,the Palm Pilot,Palm PDAs,g' %{name}.desktop
sed -i -e 's,Exec=%{name},Exec=%{_bindir}/%{name},g' %{name}.desktop
sed -i -e 's,%{name}.xpm,%{name},g' %{name}.desktop

%build
%if %cvs
./autogen.sh
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
%{makeinstall}

# jpilot use (almost) hardcoded plugins directory as:
#   BASE_DIR ABILIB EPN plugins
# which gives on a real system
#   /usr/lib/jpilot/plugins
# so fix plugins which have been installed in /usr/lib else.
mkdir -p %{buildroot}/%{_libdir}/%{name}/plugins
mv %{buildroot}/%{_libdir}/lib*.so* %{buildroot}/%{_libdir}/%{name}/plugins/
mv %{buildroot}/%{_libdir}/lib*.la %{buildroot}/%{_libdir}/%{name}/plugins/

chrpath -d %{buildroot}/%{_bindir}/%{name}*
chrpath -d %{buildroot}/%{_libdir}/%{name}/plugins/*.so.0.*

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

%post
%{update_menus}
%{update_icon_cache hicolor}

%postun 
%{clean_menus}
%{clean_icon_cache hicolor}

#%post -n %{libname} -p /sbin/ldconfig

#%postun -n %{libname} -p /sbin/ldconfig

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

%files -n %{libname}
%defattr(-,root,root)
%doc README
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc docs/plugin.html
%{_libdir}/%{name}/plugins/*.so
%{_libdir}/%{name}/plugins/*.la
%{_includedir}/*.h

