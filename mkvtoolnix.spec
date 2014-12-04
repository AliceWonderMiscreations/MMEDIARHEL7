Summary: Matroska container manipulation utilities
Name: mkvtoolnix
Version: 7.0.0
Release: 1%{?dist}
License: GPLv2+
Group: Applications/Multimedia
Source0: http://www.bunkus.org/videotools/mkvtoolnix/sources/%{name}-%{version}.tar.xz
URL: http://www.bunkus.org/videotools/mkvtoolnix/index.html
BuildRequires: boost-devel
BuildRequires: bzip2-devel
BuildRequires: desktop-file-utils
BuildRequires: expat-devel
BuildRequires: file-devel
BuildRequires: flac-devel
BuildRequires: gettext
BuildRequires: libcurl-devel
BuildRequires: libmatroska-devel
BuildRequires: libvorbis-devel
BuildRequires: lzo-devel
BuildRequires: po4a
BuildRequires: pcre-devel
BuildRequires: ruby
BuildRequires: wxGTK-devel
BuildRequires: zlib-devel

%description
Mkvtoolnix is a set of utilities to mux and demux audio, video and subtitle
streams into and from Matroska containers.

%package gui
Summary: Graphical interface for Matroska container manipulation
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Requires: hicolor-icon-theme

%description gui
Mkvtoolnix is a set of utilities to mux and demux audio, video and subtitle
streams into and from Matroska containers.

This package contains the graphical interface for these utilities.

%prep
%setup -q
sed -i -e 's/"-O3"/""/' configure*
for file in AUTHORS ChangeLog ; do
  iconv -f iso8859-1 -t utf8 $file >$file.utf && \
  touch -r $file $file.utf && \
  mv $file.utf $file
done
chmod -x src/input/r_flv.{h,cpp}

%build
%configure --with-boost-libdir=%{_libdir} --without-curl || cat config.log
./drake %{?_smp_mflags} TOOLS=1 V=1

%install
./drake DESTDIR=$RPM_BUILD_ROOT TOOLS=1 install
desktop-file-install \
  --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
  --mode=644 \
  --add-category=GTK \
  share/desktop/mkvmergeGUI.desktop
for size in 32x32 64x64 ; do
install -Dpm 644 share/icons/$size/mkvmergeGUI.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps/mkvmergeGUI.png
done
desktop-file-install \
  --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
  --mode=644 \
  share/desktop/mkvinfo.desktop
for size in 32x32 64x64 ; do
install -Dpm 644 share/icons/$size/mkvinfo.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps/mkvinfo.png
done

rm -r $RPM_BUILD_ROOT%{_docdir}/mkvtoolnix/guide

install -pm 755 src/tools/{base64tool,diracparser,ebml_validator,vc1parser} $RPM_BUILD_ROOT%{_bindir}

%find_lang %{name}

%post gui
update-desktop-database &>/dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
touch %{_datadir}/icons/hicolor &>/dev/null || :

%postun gui
update-desktop-database &>/dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
touch %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans gui
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(644,root,root,0755)
%doc AUTHORS COPYING README ChangeLog TODO
%attr(755,root,root) %{_bindir}/base64tool
%attr(755,root,root) %{_bindir}/diracparser
%attr(755,root,root) %{_bindir}/ebml_validator
%attr(755,root,root) %{_bindir}/mkvextract
%attr(755,root,root) %{_bindir}/mkvmerge
%attr(755,root,root) %{_bindir}/mkvpropedit
%attr(755,root,root) %{_bindir}/vc1parser
%{_mandir}/man1/mkvextract*
%{_mandir}/man1/mkvmerge*
%{_mandir}/man1/mkvpropedit.1*
%lang(de) %{_mandir}/de/man1/mkvextract*
%lang(de) %{_mandir}/de/man1/mkvmerge*
%lang(de) %{_mandir}/de/man1/mkvpropedit.1*
%lang(ja) %{_mandir}/ja/man1/mkvextract*
%lang(ja) %{_mandir}/ja/man1/mkvmerge*
%lang(ja) %{_mandir}/ja/man1/mkvpropedit.1*
%lang(nl) %{_mandir}/nl/man1/mkvextract*
%lang(nl) %{_mandir}/nl/man1/mkvmerge*
%lang(nl) %{_mandir}/nl/man1/mkvpropedit.1*
%lang(uk) %{_mandir}/uk/man1/mkvextract*
%lang(uk) %{_mandir}/uk/man1/mkvmerge*
%lang(uk) %{_mandir}/uk/man1/mkvpropedit.1*
%lang(zh_CN) %{_mandir}/zh_CN/man1/mkvextract*
%lang(zh_CN) %{_mandir}/zh_CN/man1/mkvmerge*
%lang(zh_CN) %{_mandir}/zh_CN/man1/mkvpropedit.1*

%files gui
%defattr(644,root,root,0755)
%doc doc/guide/en
%lang(zh_CN) %doc doc/guide/zh_CN
%attr(755,root,root) %{_bindir}/mkvinfo
%attr(755,root,root) %{_bindir}/mmg
%{_mandir}/man1/mkvinfo*
%{_mandir}/man1/mmg*
%lang(de) %{_mandir}/de/man1/mkvinfo*
%lang(de) %{_mandir}/de/man1/mmg*
%lang(ja) %{_mandir}/ja/man1/mkvinfo*
%lang(ja) %{_mandir}/ja/man1/mmg*
%lang(uk) %{_mandir}/uk/man1/mkvinfo*
%lang(uk) %{_mandir}/uk/man1/mmg*
%lang(nl) %{_mandir}/nl/man1/mkvinfo*
%lang(nl) %{_mandir}/nl/man1/mmg*
%lang(zh_CN) %{_mandir}/zh_CN/man1/mkvinfo*
%lang(zh_CN) %{_mandir}/zh_CN/man1/mmg*
%{_datadir}/applications/mkvinfo.desktop
%{_datadir}/applications/mkvmergeGUI.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/mime/packages/mkvtoolnix.xml

%changelog
* Wed Jun 18 2014 Dominik Mierzejewski <rpm@greysector.net> 7.0.0-1
- update to 7.0.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 6.9.1-2
- Rebuild for boost 1.55.0

* Sun Apr 27 2014 Dominik Mierzejewski <rpm@greysector.net> 6.9.1-1
- update to 6.9.1

* Tue Mar 04 2014 Dominik Mierzejewski <rpm@greysector.net> 6.8.0-1
- update to 6.8.0
- fixes bug #1053883

* Sat Jan 18 2014 Dominik Mierzejewski <rpm@greysector.net> 6.7.0-1
- update to 6.7.0

* Fri Dec 27 2013 Dominik Mierzejewski <rpm@greysector.net> 6.6.0-1
- update to 6.6.0
- drop obsolete/redundant specfile parts
- remove executable bit from some sources
- drop version from libmatroska-devel BR
- disable curl support (used only for online update checks)

* Sun Oct 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.5.0-1
- Update to 6.5.0
- Fix duplicate localized man pages and add lang(de)

* Thu Oct 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.4.1-1
- Update to 6.4.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 6.3.0-2
- Rebuild for boost 1.54.0

* Sat Jul 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.3.0-1
- Update to 6.3.0

* Mon Apr 29 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.2.0-1
- Update to 6.2.0

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.1.0-1
- Update to 6.1.0

* Fri Feb 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.0.0-3
- Rebuilt for f19
- Fix bogus date

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 6.0.0-2
- Rebuild for Boost-1.53.0

* Tue Jan 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.0.0-1
- Update to 6.0.0

* Mon Dec 10 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.9.0-1
- Update to 0.5.9

* Wed Sep 05 2012 Dominik Mierzejewski <rpm@greysector.net> 5.8.0-1
- update to 5.8.0

* Sun Aug 12 2012 Kevin Fenzi <kevin@scrye.com> - 5.7.0-2
- Rebuild for new boost

* Sun Jul 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.7.0-1
- Update to 5.7.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.5.0-1
- Update to 5.5.0

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.1-3
- Rebuilt for c++ ABI breakage

* Tue Jan 17 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.2.1-2
- Add BR po4a

* Thu Jan 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.2.1-1
- Update to 5.2.1
- Add BR libcurl-devel

* Sun Nov 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.0.1-1
- Update to 5.0.1

* Fri Sep 09 2011 Dan Horák <dan[at]danny.cz> - 4.9.1-3
- fix boost detection on other 64-bit arches (ax_boost_base.m4 too old)

* Sat Jul 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 4.9.1-2
- Rebuild for boost

* Thu Jul 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 4.9.1-1
- Update to 4.9.1

* Tue Feb 15 2011 Nicolas Chauvet <kwizart@gmail.com> - 4.5.0-1
- Update to 4.5.0
- Backport Fix to build with boost::filesystem3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-1
- updated to 4.4.0
- build system switched to rake -> BR: ruby

* Sun Aug 01 2010 Dominik Mierzejewski <rpm@greysector.net> 4.2.0-1
- updated to 4.2.0 (many bugfixes, see upstream changelog:
  http://www.bunkus.org/cgi-bin/gitweb.cgi?p=mkvtoolnix.git;a=blob;f=ChangeLog)
- sorted BRs alphabetically
- use upstream .desktop files
- install 64x64 icons as well
- drop vendor from desktop filenames
- add Dutch manpages
- process mimeinfo file in scriptlets

* Wed Jul 14 2010 Dan Horák <dan@danny.cz> - 4.0.0-2
- rebuilt against wxGTK-2.8.11-2

* Sat Jun 19 2010 Dominik Mierzejewski <rpm@greysector.net> 4.0.0-1
- updated to 4.0.0

* Sat May 29 2010 Dominik Mierzejewski <rpm@greysector.net> 3.4.0-1
- updated to 3.4.0
- drop unused %%{_datadir}/mkvtoolnix directory
- add build- and runtime requirements on newer libmatroska
- add runtime requirements on newer libebml due to ABI changes

* Sat Mar 27 2010 Dominik Mierzejewski <rpm@greysector.net> 3.3.0-1
- updated to 3.3.0

* Mon Feb 15 2010 Dominik Mierzejewski <rpm@greysector.net> 3.2.0-1
- updated to 3.2.0
- dropped versions from BRs, F-11 has same or newer
- added Chinese manpages

* Sat Jan 23 2010 Dominik Mierzejewski <rpm@greysector.net> 3.1.0-1
- updated to 3.1.0
  * BlueRay subtitles support
- added Japanese manpages

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 3.0.0-2
- Rebuild for Boost soname bump

* Sat Dec 26 2009 Dominik Mierzejewski <rpm@greysector.net> 3.0.0-1
- updated to 3.0.0
- dropped upstream'd patches

* Sun Dec 06 2009 Dominik Mierzejewski <rpm@greysector.net> 2.9.9-1
- updated to 2.9.9
  * new CLI tool: mkvpropedit
- fixed compilation of vc1parser

* Sun Sep 27 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.9.8-2
- Update desktop file according to F-12 FedoraStudio feature

* Wed Aug 26 2009 Dominik Mierzejewski <rpm@greysector.net> 2.9.8-1
- updated to 2.9.8
- improved summary and description for gui subpackage
- fixed installation of tools

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 06 2009 Dominik Mierzejewski <rpm@greysector.net> 2.6.0-1
- updated to 2.6.0
- dropped upstreamed patches

* Sun Mar 01 2009 Dominik Mierzejewski <rpm@greysector.net> 2.5.2-1
- updated to 2.5.2
- fix compilation
- include translated messages

* Fri Feb 27 2009 Dominik Mierzejewski <rpm@greysector.net> 2.5.1-1
- updated to 2.5.1
- dropped obsolete patches
- use new icon cache scriptlets
- add missing BR

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Dominik Mierzejewski <rpm@greysector.net> 2.4.2-1
- updated to 2.4.2
- dropped obsolete boost detection patch
- fixed segmentation fault in mmg (bug #477857)
- backported some minor fixes from current git
- fixed build on ppc64 again

* Wed Dec 17 2008 Benjamin Kosnik  <bkoz@redhat.com> 2.4.0-4
- Rebuild for boost-1.37.0.

* Mon Dec 01 2008 Dominik Mierzejewski <rpm@greysector.net> 2.4.0-3
- dropped obsolete mkvtoolnix-gcc43.patch

* Mon Dec 01 2008 Dominik Mierzejewski <rpm@greysector.net> 2.4.0-2
- fixed boost detection on ppc64 (and sparc64) (bug #473976)

* Sun Nov 30 2008 Dominik Mierzejewski <rpm@greysector.net> 2.4.0-1
- updated to 2.4.0
- rebased patch
- added new BRs
- added missing Requires: hicolor-icon-theme for hicolor icon dirs
- build and include more tools
- fixed rpmlint issues

* Sun Jun 01 2008 Dominik Mierzejewski <rpm@greysector.net> 2.2.0-1
- updated to 2.2.0
- dropped redundant BRs

* Fri Feb 15 2008 Dominik Mierzejewski <rpm@greysector.net> 2.1.0-2
- fixed build with gcc-4.3

* Sun Aug 26 2007 Dominik Mierzejewski <rpm@greysector.net> 2.1.0-1
- updated to 2.1.0
- updated license tag

* Sun Apr 15 2007 Dominik Mierzejewski <rpm@greysector.net> 2.0.2-1
- updated to 2.0.2

* Thu Feb 15 2007 Dominik Mierzejewski <rpm@greysector.net> 2.0.0-1
- updated to 2.0.0
- rebuilt against new flac

* Sat Dec 16 2006 Dominik Mierzejewski <rpm@greysector.net> 1.8.1-2
- rebuilt with new wxGTK

* Tue Dec 05 2006 Dominik Mierzejewski <rpm@greysector.net> 1.8.1-1
- updated to 1.8.1

* Sun Nov 26 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.8.0-3
- Update GTK icon cache in -gui's post(un)install phase, not main pkg's.
- Add menu entry for mkvinfo.

* Thu Nov 23 2006 Dominik Mierzejewski <rpm@greysector.net> 1.8.0-2
- moved mkvinfo and its manpage to -gui
- dropped --enable-debug from configure

* Sun Nov 19 2006 Dominik Mierzejewski <rpm@greysector.net> 1.8.0-1
- updated to 1.8.0
- prevent stripping binaries during make install
- removed sed from BRs
- made -gui Require: current version of the main package
- specfile cleanups

* Fri Jul 28 2006 Dominik Mierzejewski <rpm@greysector.net> 1.7.0-1
- updated to 1.7.0
- removed FCver dependent BRs

* Sun Apr 02 2006 Dominik Mierzejewski <rpm@greysector.net> 1.6.5-3
- added missing BRs
- enable all deps by default

* Sat Jan 07 2006 Dominik Mierzejewski <rpm@greysector.net> 1.6.5-2
- added desktop file and icon for GUI
- remove hardcoded -O3 from configure's CFLAGS

* Fri Jan 06 2006 Dominik Mierzejewski <rpm@greysector.net>
- dropped RH7.x support
- specfile cleanups

* Sun Dec 11 2005 Dominik Mierzejewski <rpm@greysector.net>
- updated to 1.6.5
- updated BuildRequires

* Thu Jul 07 2005 Dominik Mierzejewski <rpm@greysector.net>
- updated to 1.5.0

* Mon Apr 11 2005 Dominik Mierzejewski <rpm@greysector.net>
- fixed BRs for Fedoras

* Wed Jan 12 2005 Dominik Mierzejewski <rpm@greysector.net>
- fixed rebuilding under RH7.3

* Sat Jan 08 2005 Dominik Mierzejewski <rpm@greysector.net>
- updated to 1.0.1

* Sat Oct 16 2004 Dominik Mierzejewski <rpm@greysector.net>
- arranged sections in correct order
- split GUI into separate package
- added some bconds

* Sat Jan 03 2004 Ronald Bultje <rbultje@ronald.bitfreak.net
- set this thing up
