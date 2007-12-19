%define name jpilot
%define name_plugin %{name}_plugin
%define major 0
%define lib_name %mklibname %{name_plugin} %{major}
%define version 0.99.9
%define release %mkrel 2
%define pilot_link_version 0.12.0

Name:		%{name}
Summary:	Palm pilot desktop for Linux
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Communications
URL:		http://www.jpilot.org/
Source0:	http://jpilot.org/%{name}-%{version}.tar.bz2
Patch1:		jpilot-0.99.4-usbinfo.patch
Patch2:		jpilot-0.99.1u-plugins-improvement.patch
Patch3:		jpilot-0.99.7-misc.patch
# (fc) 0.99.2-2mdv fix crash
Patch4:		jpilot-0.99.8-fixcrash.patch
Requires:	pilot-link >= %{pilot_link_version} %{lib_name} = %{version}
BuildRequires:	ImageMagick
BuildRequires:	chrpath
BuildRequires:  desktop-file-utils
BuildRequires:	gtk2-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pilot-link-devel >= %{pilot_link_version}
BuildRequires:	readline-devel
BuildRequires:	perl-XML-Parser

%description
J-Pilot is a desktop organizer application for the palm pilot that runs
under Linux and UNIX.  It is similar in functionality to the one that 3com
distributes for a well known rampant legacy operating system.

%package -n	%{lib_name}
Summary:	Shared libraries for jpilot
Group:		Communications

%description -n	%{lib_name}
J-Pilot is a desktop organizer application for the palm pilot that runs
under Linux and UNIX.  It is similar in functionality to the one that 3com
distributes for a well known rampant legacy operating system.

The shared libraries required for jpilot.

%package -n	%{lib_name}-devel
Summary:	Library and header file needed for jpilot plugin development
Group:		Communications
Requires:	%{lib_name} = %{version}
Provides:	%_lib%{name_plugin}-devel = %{version} %{name_plugin}-devel = %{version}

%description -n	%{lib_name}-devel
J-Pilot is a desktop organizer application for the palm pilot that runs
under Linux and UNIX.  It is similar in functionality to the one that 3com
distributes for a well known rampant legacy operating system.

The library and header file required for plugin development

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
#patch4 -p1 -b .fixcrash

%build
%if %_lib == lib64
  %define conf_args enable_libsuffix=64
%else 
  %define conf_args ""
%endif
#%define optflags -g -O2
%configure2_5x %conf_args
%make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_mandir}/man1,%{_bindir}}
%{makeinstall}

# jpilot use (almost) hardcoded plugins directory as :
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

perl -p -i -e 's|%{buildroot}||' %{buildroot}/%{_libdir}/*la

mkdir -p %{buildroot}/%{_includedir}
install -m 644 {libplugin,prefs}.h %{buildroot}%{_includedir}/

# use builtin icons and ImageMagick to do the conversion.
mkdir -p %{buildroot}/%{_iconsdir}/{mini,large}
convert -resize 16x16 icons/jpilot-icon1.xpm %{buildroot}/%{_iconsdir}/mini/jpilot.png
convert -resize 32x32 icons/jpilot-icon1.xpm %{buildroot}/%{_iconsdir}/jpilot.png
convert -resize 48x48 icons/jpilot-icon1.xpm %{buildroot}/%{_iconsdir}/large/jpilot.png

mkdir -p %{buildroot}%{_menudir}
cat << EOF > %{buildroot}%{_menudir}/%{name}
?package(jpilot): \
  needs="x11" \
  section="Office/Communications/PDA" \
  title="J-Pilot" \
  longtitle="A tool for your palm pilot" \
  icon="jpilot" \
  command="jpilot" \
  xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Communications-PDA" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang %{name}

%post
%update_menus

%postun 
%clean_menus

#%post -n %{lib_name} -p /sbin/ldconfig

#%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog README TODO
%doc docs/manual.html docs/jpilot-*.png docs/jpilot-*.jpg
%{_bindir}/*
%{_datadir}/jpilot
%{_datadir}/icons/*png
%{_datadir}/icons/*/*png
%{_datadir}/applications/*
%{_menudir}/jpilot
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-,root,root)
%doc COPYING README
%dir %{_libdir}/jpilot
%dir %{_libdir}/jpilot/plugins
%{_libdir}/jpilot/plugins/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc docs/plugin.html
%{_libdir}/jpilot/plugins/*.so
%{_libdir}/jpilot/plugins/*.la
%{_includedir}/*.h

