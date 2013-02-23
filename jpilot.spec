%define name_plugin	%{name}_plugin

%define pilot_link_version 0.12.5
%define	_disable_ld_no_undefined 1

Summary:	Palm pilot desktop for Linux
Name:		jpilot
Version:	1.8.1
Release:	1
License:	GPLv2
Group:		Communications
URL:		http://www.jpilot.org/
Source0:	http://jpilot.org/%{name}-%{version}.tar.gz
Patch2:		jpilot-0.99.1u-plugins-improvement.patch
Patch4:		jpilot-1.8.0-linkage.patch
#Patch5:		jpilot-1.6.2-libdir-fix.patch
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
%patch2 -p1 -b .plugins
%patch4 -p0 -b .linkage
#patch5 -p0 -b .libdir
%patch7 -p0 -b .desktop

%build
export ABILIB="%_lib"
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
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %{name}

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

%files expense
%{_libdir}/%{name}/plugins/libexpense.so

%files keyring
%{_libdir}/%{name}/plugins/libkeyring.so

%files synctime
%{_libdir}/%{name}/plugins/libsynctime.so

%files devel
%doc docs/plugin.html
%{_includedir}/*.h

%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.8.0-2mdv2011.0
+ Revision: 665831
- mass rebuild

* Sun Sep 05 2010 Bruno Cornec <bcornec@mandriva.org> 1.8.0-1mdv2011.0
+ Revision: 576106
- Remove old upstream sources now useless
- Update jpilot to upstream 1.8.0

* Fri Apr 09 2010 Funda Wang <fwang@mandriva.org> 1.6.2-3mdv2010.1
+ Revision: 533332
- rebuild

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 1.6.2-2mdv2010.1
+ Revision: 511583
- rebuilt against openssl-0.9.8m

* Mon Jun 15 2009 Funda Wang <fwang@mandriva.org> 1.6.2-1mdv2010.0
+ Revision: 385967
- New version 1.6.2

  + Christophe Fergeau <cfergeau@mandriva.com>
    -fix -Wformat warnings

* Mon Nov 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.99.10-0.20071220.5mdv2009.1
+ Revision: 301744
- package the plugins correctly
- fix build (libtool fixes)
- rebuilt against new libxcb

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - remove commented ldconfig calls (won't be needed anymore anyway)

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 0.99.10-0.20071220.3mdv2008.1
+ Revision: 189637
- Fix lib group
- protect major

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 0.99.10-0.20071220.2mdv2008.1
+ Revision: 189601
- Fix devel group

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag

* Fri Dec 21 2007 Adam Williamson <awilliamson@mandriva.org> 0.99.10-0.20071220.1mdv2008.1
+ Revision: 136103
- use NOCONFIGURE=1 to skip configure after running autogen.sh, otherwise it fails on x86-64 as it can't find the pilot-link libs
- cvs buildrequires intltool
- buildrequires gettext-devel (for cvs)
- rebuild for new era
- new library policy
- fd.o icons
- correct various XDG menu issues
- drop legacy menu
- bump to current CVS (Debian does the same, apparently much improved over last release)
- slightly modify descriptions
- spec clean

  + Thierry Vignaud <tv@mandriva.org>
    - do not hardcode icon extension
    - kill re-definition of %%buildroot on Pixel's request


* Fri Dec 22 2006 Christiaan Welvaart <cjw@daneel.dyndns.org>
+ 2006-12-22 13:44:42 (101484)
- add BuildRequires: perl-XML-Parser

* Wed Nov 01 2006 Stefan van der Eijk <stefan@mandriva.org>
+ 2006-11-01 20:08:43 (75070)
fix usbinfo patch

* Wed Nov 01 2006 Stefan van der Eijk <stefan@mandriva.org>
+ 2006-11-01 17:48:24 (75051)
decompress patches

* Tue Oct 31 2006 Stefan van der Eijk <stefan@mandriva.org>
+ 2006-10-31 12:33:16 (74308)
0.99.9

* Tue Oct 31 2006 Stefan van der Eijk <stefan@mandriva.org>
+ 2006-10-31 08:36:36 (74118)
Import jpilot

* Tue Sep 19 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.99.8-3mdv2007.0
- Rebuild

* Wed Sep 06 2006 Frederic Crozat <fcrozat@mandriva.com> 0.99.8-2mdv2007.0
- Patch4: fix crash at startup
- Rebuild for pilot-link 0.12.0
- migrate menu to XDG

* Sun Jul 02 2006 Stefan van der Eijk <stefan@mandriva.org> 0.99.8-1
- update from Cris B <cris@beebgames.com>
  - 0.99.8
  - switch to gtk2

* Tue Jan 03 2006 Stefan van der Eijk <stefan@eijk.nu> 0.99.7-6mdk
- Rebuild (libcrypto.so.0.9.8)

* Wed May 04 2005 Stew Benedict <sbenedict@mandriva.com> 0.99.7-5mdk
- really fix 64bit build, thx Gwenole

* Wed May 04 2005 Stew Benedict <sbenedict@mandriva.com> 0.99.7-4mdk
- fix 64bit build, mkrel

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.99.7-3mdk
- rebuild for new slang
- fix summary-ended-with-dot

* Sat Aug 21 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.99.7-2mdk
- fix typo in menu entry

* Thu Jun 03 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.99.7-1mdk
- 0.99.7

* Thu Feb 12 2004 David Baudens <baudens@mandrakesoft.com> 0.99.6-2mdk
- Fix menu

