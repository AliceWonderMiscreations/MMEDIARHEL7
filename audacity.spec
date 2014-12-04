# Compile options:

Name: audacity

Version: 2.0.5
Release: 3%{?dist}
Summary: Multitrack audio editor
Group:   Applications/Multimedia
License: GPLv2
URL:     http://audacity.sourceforge.net

%define realname audacity

# use for upstream source releases:
#Source0: http://downloads.sf.net/sourceforge/audacity/audacity-minsrc-%#{version}-beta.tar.bz2
Source0: http://audacity.googlecode.com/files/audacity-minsrc-%{version}.tar.xz
%define tartopdir audacity-src-%{version}

Source1: http://audacity.googlecode.com/files/audacity-manual-%{version}.zip

# Patch1: audacity-2.0.4-libmp3lame-default.patch
# Patch2: audacity-1.3.9-libdir.patch
# add audio/x-flac
# remove audio/mpeg, audio/x-mp3
# enable startup notification
# add categories Sequencer X-Jack AudioVideoEditing for F-12 Studio feature
# Patch3: audacity-2.0.2-desktop.in.patch
# Patch4: audacity-2.0.4-equalization-segfault.patch# BZ#1076795
Patch0001: 0001-BZ-1076795-Removed-bundled-copy-of-expat.h.patch

BuildRequires: alsa-lib-devel
BuildRequires: desktop-file-utils
BuildRequires: expat-devel
BuildRequires: flac-devel
BuildRequires: gettext
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: ladspa-devel
BuildRequires: libid3tag-devel
BuildRequires: taglib-devel
BuildRequires: libogg-devel
BuildRequires: libsndfile-devel
BuildRequires: libvorbis-devel
BuildRequires: portaudio-devel >= 19-16
BuildRequires: soundtouch-devel
BuildRequires: soxr-devel
BuildRequires: vamp-plugin-sdk-devel >= 2.0
BuildRequires: zip
BuildRequires: zlib-devel
BuildRequires: wxGTK-devel
BuildRequires: libmad-devel twolame-devel lame-devel
# For new symbols in portaudio
Requires:      portaudio%{?_isa} >= 19-16

%description
Audacity is a cross-platform multitrack audio editor. It allows you to
record sounds directly or to import files in various formats. It features
a few simple effects, all of the editing features you should need, and
unlimited undo. The GUI was built with wxWidgets and the audio I/O
supports PulseAudio, OSS and ALSA under Linux.

%package manual
Summary: manual for Audacity - offline install
BuildArch: noarch
# -manual suits either audacity or audacity-freeworld; both create the path:
Requires: /usr/bin/audacity

%description manual
Audacity Manual can be installed locally if preferred, or accessed on-line
if internet connection is available.
For the most up to date manual content, use the on-line manual.

%prep
%setup -q -n %{tartopdir}

%patch0001 -p1

# Substitute hardcoded library paths.
# %patch1 -b .libmp3lame-default
# %patch2 -p1 -b .libdir
for i in src/effects/ladspa/LoadLadspa.cpp src/AudacityApp.cpp src/export/ExportMP3.cpp
do
    sed -i -e 's!__RPM_LIBDIR__!%{_libdir}!g' $i
    sed -i -e 's!__RPM_LIB__!%{_lib}!g' $i
done
grep -q -s __RPM_LIB * -R && exit 1

# Substitute occurences of "libmp3lame.so" with "libmp3lame.so.0".
for i in locale/*.po src/export/ExportMP3.cpp
do
    sed -i -e 's!libmp3lame.so\([^.]\)!libmp3lame.so.0\1!g' $i
done

# %patch3 -b .desktop.old
# %patch4 -b .2.0.4-equalization-segfault.patch


%build
%configure \
    --with-help \
    --with-libsndfile=system \
    --with-libsoxr=system \
    --without-libresample \
    --without-libsamplerate \
    --with-libflac=system \
    --with-ladspa \
    --with-vorbis=system \
    --with-id3tag=system \
    --with-expat=system \
    --with-soundtouch=system \
    --with-libvamp=system \
    --with-portaudio=system \
    --without-ffmpeg \
    --with-libmad=system \
    --with-libtwolame=system \
    --with-lame=system

# ensure we use the system headers for these, note we do this after
# configure as it wants to run sub-configures in these dirs
for i in ffmpeg libresample libsoxr libvamp portaudio-v19; do
   rm -rf lib-src/$i
done

# _smp_mflags cause problems
make


%install
%make_install

# Audacity 1.3.8-beta complains if the help/manual directories
# don't exist.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/help/manual

%{find_lang} %{realname}

desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
%if 0%{?fedora} && 0%{?fedora} < 19
        --vendor fedora --delete-original                          \
%endif
        $RPM_BUILD_ROOT%{_datadir}/applications/audacity.desktop

# audacity manual must be unzipped to correct location
unzip %{SOURCE1} -d $RPM_BUILD_ROOT%{_datadir}/%{realname}


%post
umask 022
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
umask 022
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{realname}.lang
%{_bindir}/%{realname}
%dir %{_datadir}/%{realname}
%{_datadir}/%{realname}/EQDefaultCurves.xml
%{_datadir}/%{realname}/nyquist/
%{_datadir}/%{realname}/plug-ins/
%{_mandir}/man*/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/%{realname}.*
%{_datadir}/mime/packages/*
%doc %{_datadir}/doc/*
%doc lib-src/libnyquist/nyquist/license.txt lib-src/libnyquist/nyquist/Readme.txt

%files manual
%{_datadir}/%{realname}/help/


%changelog
* Tue Oct 07 2014 Alice Wonder <alicewonder@shastaherps.org> - 2.0.5-3
- Build for AWEL w/ mp3 support

* Mon Mar 17 2014 Darryl L. Pierce <dpierce@redhat.com> - 2.0.5-2
- Removed bundled expat.h from sources.
- Resolves: BZ#1076795

* Tue Feb 25 2014 Darryl L. Pierce <dpierce@redhat.com> - 2.0.5-1
- Rebased on Audacity 2.0.5.

* Sun Sep 22 2013 David Timms <iinet.net.au@dtimms> - 2.0.4-2
- Add upstream patch to avoid segfault when starting Effects|Equalization

* Sat Sep 14 2013 David Timms <iinet.net.au@dtimms> - 2.0.4-1
- update to upstream release 2.0.4
- rebase audacity-2.0.1-libmp3lame-default

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.3-2
- include the readme/license for the nyquist/xlisp bits

* Sat May  4 2013 Hans de Goede <hdegoede@redhat.com> - 2.0.3-1
- New upstream release 2.0.3 (rhbz#951001)
- This release adds aarch64 support (rhbz#925052)
- Use system portaudio
- Add icon-cache update scriptlets

* Sun Feb 10 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 2.0.2-3
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines

* Tue Sep 04 2012 Dan Horák <dan[at]danny.cz> - 2.0.2-2
- fix build on non-x86 arches

* Mon Aug 27 2012 David Timms <iinet.net.au@dtimms> - 2.0.2-1
- update to 2.0.2 final
- update to manual-2.0.2
- adjust manual extract path to suit changes to manual.zip

* Thu Jul 19 2012 David Timms <iinet.net.au@dtimms> - 2.0.1-1
- update to 2.0.1 final
- rebase libmp3lame-default.patch
- rebase desktop.in.patch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 David Timms <iinet.net.au@dtimms> - 2.0.0-1
- update to 2.0.0 final

* Sun Mar 11 2012 David Timms <iinet.net.au@dtimms> - 2.0.0-0.9.rc9
- update to 2.0.0 release candidate 9
- drop upstreamed glib2 include patch

* Tue Mar  6 2012 David Timms <iinet.net.au@dtimms> - 2.0.0-0.8.rc8
- update to 2.0.0 release candidate 8 for testing only

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.4.rc3
- Rebuilt for c++ ABI breakage

* Wed Feb 22 2012 David Timms <iinet.net.au@dtimms> - 2.0.0-0.3.rc3
- update to 2.0.0 release candidate 3

* Sat Feb 18 2012 David Timms <iinet.net.au@dtimms> - 2.0.0-0.2.rc1.20120218svn11513
- update to release candidate from svn snapshot
- update to use online manual for 2.0 series

* Sun Feb  5 2012 David Timms <iinet.net.au@dtimms> - 2.0.0-0.1.alpha20120205svn11456
- update to 2.0.0 alpha svn snapshot
- delete accepted ffmpeg-0.8.y patch

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.14-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 David Timms <iinet.net.au@dtimms> - 1.3.14-0.5
- fix Source1 help reference (again).

* Tue Dec 13 2011 David Timms <iinet.net.au@dtimms> - 1.3.14-0.4
- update to 1.3.14 beta release

* Thu Dec  8 2011 David Timms <iinet.net.au@dtimms> - 1.3.14-0.3.alpha20111101svn11296
- add ffmpeg-0.8 patch from Leland Lucius
- add test patch to workaround gtypes-include problem

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.3.14-0.2.alpha20111101svn11296
- Rebuild for new libpng

* Tue Nov  1 2011 David Timms <iinet.net.au@dtimms> - 1.3.14-0.1.alpha20111101svn11296
- update to 1.3.14 alpha svn snapshot

* Wed May  4 2011 David Timms <iinet.net.au@dtimms> - 1.3.13-0.4.beta
- add Requires on audacity folder path to pick up either audacity* package

* Sat Apr 30 2011 David Timms <iinet.net.au@dtimms> - 1.3.13-0.4.beta
- fix files and dir ownership including -manual files in the main package

* Tue Apr 26 2011 David Timms <iinet.net.au@dtimms> - 1.3.13-0.3.beta
- add audacity manual help file Source and subpackage

* Sun Apr 24 2011 David Timms <iinet.net.au@dtimms> - 1.3.13-0.2.beta
- upgrade to 1.3.13-beta
- drop patches included in upstream release
- convert desktop file to a patch against new upstream .desktop file.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-0.7.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec  7 2010 Manuel F Martinez <manpaz@bashlinux.com> - 1.3.12-0.6.beta
- Create gcc45 patch to fix issues with configure in portmixer

* Wed Jul 14 2010 Dan Horák <dan@danny.cz> - 1.3.12-0.5.beta
- rebuilt against wxGTK-2.8.11-2

* Mon Jun 28 2010 David Timms <iinet.net.au@dtimms> - 1.3.12-0.4.beta
- mods to ease diffs between builds for fedora and full

* Mon Jun 28 2010 David Timms <iinet.net.au@dtimms> - 1.3.12-0.3.beta
- really package new icons found in icons/hicolor

* Mon Jun 28 2010 David Timms <iinet.net.au@dtimms> - 1.3.12-0.2.beta
- mod tartopdir to use package version macro

* Mon Jun 28 2010 David Timms <iinet.net.au@dtimms> - 1.3.12-0.1.beta
- upgrade to 1.3.12-beta
- package new icons found in icons/hicolor

* Thu Jan 21 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.11-0.1.beta
- Upgrade to 1.3.11-beta.

* Thu Jan 21 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.10-0.4.beta
- Add audio/x-flac to .desktop file (#557335).
- Create fresh .desktop file patch. Enable startup notification.

* Sat Jan  9 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.10-0.3.beta
- Merge improved resample patch from Richard Ash.

* Mon Dec 28 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.10-0.2.beta
- Patch resampling call to not set end_of_input flag for all sample buffers.

* Fri Dec  4 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.10-0.1.beta
- Upgrade to 1.3.10-beta.

* Fri Dec  4 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.9-0.5.beta
- Prevent race-condition segfault with Sound Activated Recording (#544125).

* Wed Sep 23 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.3.9-0.4.beta
- Update desktop file according to F-12 FedoraStudio feature

* Mon Sep 14 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.9-0.3.beta
- add patch to fix LabelTrack popup

* Sat Sep 12 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.9-0.2.beta
- add wxGTK work-around patches to fix LabelTrack crash
  (shall fix #520917 and similar race-conditions)

* Thu Sep  3 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.9-0.1.beta
- upgrade to 1.3.9-beta
- upstream's changes in the device prefs code make the audiodevdefaults
  patch unnecessary afaic see

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-0.3.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.8-0.2.beta
- glib2 2.21.1's gio in Rawhide F-12 introduces a GSocket that
  conflicts with wxGTK's GSocket class (gsocket.h): as a work-around,
  include less glib headers

* Mon Jul 20 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.8-0.1.beta
- upgrade to 1.3.8-beta
- BR taglib-devel
- patches merged/obsoleted upstream:
  audacity-1.3.7-portaudio-non-mmap-alsa.patch
  audacity-1.3.7-repeat.patch
  audacity-1.3.6-flac-import.patch

* Wed May 13 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.7-0.7.beta
- retag up-to-date files and copy to F-10/F-11

* Mon Mar  2 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.7-0.6.beta
- revise default device names patch, so it doesn't save the defaults

* Sun Mar  1 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.7-0.5.beta
- show default device names in Audio I/O preferences

* Sat Feb 28 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.7-0.4.beta
- remove no longer needed default hostapi hunk of the non-mmap-alsa patch

* Sat Feb 28 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.7-0.3.beta
- F-10/F-9 only: patch to build with older Vamp API 1.3
- upgrade to 1.3.7-beta pkg from test branch in Fedora cvs

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-0.13.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.12.beta
- buildrequire >= 2.0 of Vamp SDK (because we adjust the include paths
  and to avoid that the unpatched local copy is used if system version
  is too old)

* Fri Jan  2 2009 David Timms <iinet.net.au@dtimms> - 1.3.5-0.11.beta
- add PortAudio non mmap alsa patch (Kevin Kofler) bz 445644
  allows record and playback through pulseaudio

* Wed Dec 17 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.10.beta
- patch include paths for changes in new vamp-plugin-sdk-devel

* Wed Dec 17 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.9.beta
- rebuild in Rawhide for new SONAME in vamp-plugin-sdk
- BR wxGTK-devel for rename of wxGTK2-devel 

* Tue Nov  4 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.8.beta
- insert a guard in ImportFLAC next to the import assertion

* Tue Nov  4 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.7.beta
- BR vamp-plugin-sdk-devel
- no longer build with included Vamp API, also drop Vamp multilib patch

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.6.beta
- rediff some patches for Fedora fuzz=0 pedantry

* Sun Jun  8 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.5.beta
- fix bad fr.po that makes Fichier>Open dialog too wide

* Thu May 15 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.4.beta
- desktop-file: drop deprecated Encoding, drop Icon file extension

* Thu May 15 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.3.beta
- merge 1.3.5-beta from test branch

* Fri May  9 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.2.beta
- update to 1.3.5-beta
- expat2 patch merged upstream
- scriptlets: run update-desktop-database without path
- drop scriptlet dependencies

* Mon May  5 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.5-0.1.rc3.20080505cvs
- update to 1.3.5-rc3 cvs snapshot
- ExportMP3.cpp libdir patch obsolete

* Sat May  3 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.4-0.7.20080123cvs
- check ownership of temporary files directory (#436260) (CVE-2007-6061)

* Sat Apr 12 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.4-0.6.20080123cvs
- set a default location for libmp3lame.so.0 again

* Fri Mar 21 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.4-0.5.20080123cvs
- package the old 1.3.2-beta and a post 1.3.4-beta snapshot in the
  same package -- users may stick to the older one, but please help
  with evaluating the newer one
- merge packaging changes from my 1.3.3/1.3.4 test packages:
- build newer release with wxGTK 2.8.x  
- BR soundtouch-devel  and  --with-soundtouch=system
- drop obsolete patches: resample, mp3 export, destdir, FLAC, fr

* Fri Mar 21 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.2-20
- make soundtouch and allegro build with RPM optflags

* Sun Feb 10 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.2-19
- rawhide: patch for JACK 0.109.0 API changes (jack_port_lock/unlock removal).
- rebuilt for GCC 4.3 as requested by Fedora Release Engineering
- subst _libdir in ladspa plugin loader

* Thu Jan  3 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.2-18
- Patch for GCC 4.3.0 C++.

* Fri Nov 16 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.2-17
- rebuilt for FLAC 1.1.4 -> 1.2.x upgrade, which broke FLAC import

* Tue Aug 28 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.2-16
- rebuilt for new expat (#195888)

* Tue Aug 21 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.2-15
- rebuild per request on fedora-devel-list
- clarify licence (GPLv2)

* Mon Mar  5 2007 Michael Schwendt <mschwendt@fedoraproject.org>
- add umask 022 to scriptlets

* Sat Feb 24 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.2-14
- patch for FLAC 1.1.4 API compatibility

* Sat Feb 24 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 1.3.2-13
- patch ExportMP3.cpp (MPEG-2 Layer III bitrates resulted in
  broken/empty files)
- convert locale related perl substitutions into patches (safer)
- configure with portaudio/portmixer defaults
- drop category Application from desktop file
- fix the libmp3lame.so.0 subst
- subst _libdir in libmp3lame search 
- use sed instead of perl

* Fri Feb 23 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-12
- build with wxGTK 2.6 compatibility package

* Sun Feb 18 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-11.20070106cvs
- added patch for compiling with libsamplerate

* Thu Feb 15 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-9.20070106cvs
- disable flac for now

* Thu Feb 15 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-8.20070106cvs
- compile with jack

* Mon Feb  5 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-7.20070106cvs
- compile with libsamplerate

* Mon Jan 22 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-6.20070106cvs
- convert french locale to iso-8859-1

* Sat Jan  6 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-5.20070106cvs
- corrected cvs date

* Sat Jan  6 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-3.cvs20060106
- update to cvs

* Fri Jan  5 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-2
- remove -msse flag for ppc

* Fri Jan  5 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.3.2-1
- new version 1.3.2

* Tue Jan  2 2007 Gerard Milmeister <gemi@bluewin.ch> - 1.2.6-1
- new version 1.2.6

* Sat Nov 11 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.2.5-3
- correct mime types in .desktop file
- msse flag only on intel

* Fri Nov  3 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.2.5-2
- remove -msse flag for ppc

* Fri Nov  3 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.2.5-1
- new version 1.2.5

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 1.2.4-0.2.b
- Rebuild for FE6

* Fri Mar 17 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2.4-0.1.b
- Update to 1.2.4b (stable release).
- Follow upstream recommendation and use the GTK+ 1.x wxGTK.
  This is because of various issues with fonts/layout/behaviour.
- Build with compat-wxGTK-devel.
- Modify build section to find wx-2.4-config instead of wx-config.

* Fri May 20 2005 David Woodhouse <dwmw2@infradead.org> - 1.2.3-5
- Bump release number again due to spurious build system failure and
  the fact that the build system seems to be ignoring repeated build
  requests for the previous version.

* Fri May 20 2005 David Woodhouse <dwmw2@infradead.org> - 1.2.3-4
- Add more possible MIME types for ogg which may be seen even though
  they're not standard.

* Thu Apr  7 2005 Gerard Milmeister <gemi@bluewin.ch> - 1.2.3-3
- Build gtk2 version by default

* Thu Apr  7 2005 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt

* Tue Apr  5 2005 Gerard Milmeister <gemi@bluewin.ch> - 1.2.3-2
- Rebuild to pick a new FLAC dependencies

* Sat Nov 20 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:1.2.3-1
- New Version 1.2.3

* Sat Oct 30 2004 Michael Schwendt <mschwendt@fedoraproject.org> - 0:1.2.2-0.fdr.1
- Update to 1.2.2, patch aboutdialog to be readable with wxGTK.

* Mon May 10 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:1.2.1-0.fdr.1
- New Version 1.2.1

* Sun Apr 11 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:1.2.0-0.fdr.2
- Fix for Language.cpp restored

* Tue Mar  2 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:1.2.0-0.fdr.1
- New Version 1.2.0

* Mon Nov 24 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:1.2.0-0.fdr.4.pre3
- Added icon
- Separated mp3 plugin

* Sun Nov 23 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:1.2.0-0.fdr.2.pre3
- Changes to specfile

* Sun Nov  2 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:1.2.0-0.fdr.1.pre3
- New upstream version 1.2.0-pre3

* Sat Oct 25 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:1.2.0-pre2.fdr.1
- First Fedora release

