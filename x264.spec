%global snapshot 20140921
%global branch   2245-stable
%global relmod .1
%{?_x264_bootstrap:
%global _without_gpac 1
%global _without_libavformat 1
%global relmod .0bootstrap
}
%global _without_gpac 1
#Whitelist of arches with dedicated ASM code
%ifnarch x86_64 i686 %{arm} ppc ppc64 %{sparc}
%global _without_asm 1
%endif

Summary: H264/AVC video streams encoder
Name: x264
#from version.sh - pointver
Version: 0.142
Release: 6.%{snapshot}%{?dist}%{relmod}
License: GPLv2+
Group: System Environment/Libraries
URL: http://developers.videolan.org/x264.html
Source0: %{name}-snapshot-%{snapshot}-%{branch}.tar.bz2
Source1: x264-snapshot.sh
%{!?_without_gpac:BuildRequires: gpac-devel-static zlib-devel}
%{!?_without_libavformat:BuildRequires: ffmpeg-devel}
%{?_with_ffmpegsource:BuildRequires: ffmpegsource-devel}
%{?_with_visualize:BuildRequires: libX11-devel}
%{!?_without_asm:BuildRequires: yasm >= 1.0.0}
Requires: %{name}-libs = %{version}-%{release}

%description
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the frontend.

%package libs
Summary: Library for encoding H264/AVC video streams
Group: Development/Libraries

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package devel
Summary: Development files for the x264 library
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the development files.

%define x_configure \
./configure \\\
  --prefix=%{_prefix} \\\
  --exec-prefix=%{_exec_prefix} \\\
  --bindir=%{_bindir} \\\
  --includedir=%{_includedir} \\\
  --extra-cflags="$RPM_OPT_FLAGS" \\\
  %{?_with_visualize:--enable-visualize} \\\
  %{?_without_libavformat:--disable-lavf} \\\
  %{!?_with_ffmpegsource:--disable-ffms} \\\
  %{?_without_asm:--disable-asm} \\\
  --enable-debug \\\
  --enable-shared \\\
  --system-libx264 \\\
  --enable-pic


%prep
%setup -q -n %{name}-snapshot-%{snapshot}-%{branch}
#%%patch0 -p1 -b .nover
%ifarch i686
mkdir simd
cp -a `ls -1|grep -v simd` simd/
%endif

%build
%{x_configure}\
  --host=%{_target_platform} \
  --libdir=%{_libdir} \
%ifarch i686 armv5tel armv6l
  --disable-asm \
%endif

%{__make} %{?_smp_mflags}
%ifarch i686
pushd simd
%{x_configure}\
  --host=%{_target_platform} \
  --libdir=%{_libdir}/sse2 \

%{__make} %{?_smp_mflags}
popd
%endif

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
%ifarch i686
pushd simd
%{__make} DESTDIR=%{buildroot} install
rm %{buildroot}%{_libdir}/*/pkgconfig/x264.pc
popd
%endif

#Fix timestamp on x264 generated headers
touch -r %{buildroot}%{_includedir}/x264.h %{buildroot}%{_includedir}/x264_config.h


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(644, root, root, 0755)
%doc AUTHORS COPYING
%attr(755,root,root) %{_bindir}/x264

%files libs
%defattr(644, root, root, 0755)
%{_libdir}/libx264.so.*
%ifarch i686
%{_libdir}/sse2/libx264.so.*
%endif

%files devel
%defattr(644, root, root, 0755)
%doc doc/*
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/libx264.so
%{_libdir}/pkgconfig/%{name}.pc
%ifarch i686
%{_libdir}/sse2/libx264.so
%endif

%changelog
* Mon Sep 22 2014 Alice Wonder <rpmbuild@domblogger.net> - 0.142-6.20140921
- Updated snapshot, define macro to build boostrap.
- Disable gpac for now (will re-enable later)

* Tue Jun 19 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.120-5.20120303
- Un-boostrap

* Tue May 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.120-5.20120303
- Forward rhel patch
- Disable ASM on armv5tel armv6l
- Add --with bootstrap conditional
- Use %%{_isa} for devel requires

* Tue Mar 6 2012 Sérgio Basto <sergio@serjux.com> - 0.120-2.20120303
- Enable libavformat , after compile ffmeg with 0.120-1

* Sat Mar 3 2012 Sérgio Basto <sergio@serjux.com> - 0.120-1.20120303
- Change release number, upstream have release numbers at least on stable branch and as ffmpeg
  reported.
- Update to 20120303
- Update x264-nover.patch, as suggest by Joseph D. Wagner <joe@josephdwagner.info> 
- Dropped obsolete Buildroot and Clean.
- add BuildRequires: zlib-devel to enable gpac.

* Wed Feb 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.34.20120125
- Rebuilt for F-17 inter branch

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.33.20120125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.32.20120125
- Update to 20120125

* Mon Aug 22 2011 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.31.20110811
- 20110811 snapshot (ABI 116)
- fix snapshot script to include version.h properly
- link x264 binary to the shared library

* Thu Jul 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.30.20110714
- Update to 20110714 stable branch (ABI 115)
- Convert x264-snapshot to git (based on ffmpeg script).
- New Build Conditionals --with ffmpegsource libavformat
- Remove shared and strip patches - undeeded anymore
- Remove uneeded convertion of AUTHORS

* Mon Jan 10 2011 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.29.20110227
- 20110227 snapshot (ABI bump)

* Tue Jul 06 2010 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.28.20100706gitd058f37
- 20100706 snapshot (ABI bump)
- drop old Obsoletes:

* Thu Apr 29 2010 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.27.20100429gitd9db8b3
- 20100429 snapshot
- s/%%{ix86}/i686 (rfbz #1075)
- ship more docs in -devel

* Sat Jan 16 2010 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.26.20100116git3d0f110
- 20100116 snapshot (SO version bump)
- don't remove config.h and don't re-run version.sh
- link x264 binary to the shared library
- really don't strip if debug is enabled

* Mon Oct 26 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.26.20091026gitec46ace7
- 20091026 snapshot

* Thu Oct 15 2009 kwizart <kwizart at gmail.com > -  0.0.0-0.25.20091007git496d79d
- Update to 20091007git
- Move simd to %%{_libdir}/sse2

* Thu Mar 26 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.24.20090319gitc109c8
- Tue Mar 26 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.24.20090319gitc109c8
- 20090319 snapshot
- build with static gpac
- fix build on ppc

* Tue Feb 10 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.23.20090119git451ba8d
- 20090119 snapshot
- fix BRs for build-time options

* Sat Dec 20 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.22.20081213git9089d21
- rebuild against new gpac

* Sat Dec 13 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.21.20081213git9089d21
- fix the libs split on x86

* Sat Dec 13 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.20.20081213git9089d21
- 20081213 snapshot
- drop the libs split on x86, it doesn't work right for P3/AthlonXP
- drop obsolete patch

* Thu Dec 04 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.19.20081202git71d34b4.1
- fix compilation on ppc

* Tue Dec 02 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.19.20081202git71d34b4
- 20081202 snapshot
- bring back asm optimized/unoptimized libs split
- rebase and improve patch
- GUI dropped upstream
- dropped redundant BRs

* Mon Nov 17 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.18.20080905
- partially revert latest changes (the separate sse2 libs part) until selinux
  policy catches up

* Fri Nov 07 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.17.20080905
- build libs without asm optimizations for less capable x86 CPUs (livna bug #2066)
- fix missing 0 in Obsoletes version (never caused any problems)

* Fri Sep 05 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.16.20080905
- 20080905 snapshot
- use yasm on all supported arches
- include mp4 output support via gpac by default
- drop/move obsolete fixups from %%prep
- fix icon filename in desktop file

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.0.0-0.15.20080613
- rebuild

* Sat Jun 14 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.14.20080613
- 20080613 snapshot (.so >= 59 is required by current mencoder)

* Mon May 05 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.13.20080420
- 20080420 snapshot
- split libs into a separate package
- svn -> git
- drop obsolete execstack patch
- fixed summaries and descriptions

* Wed Feb 27 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.12.20080227
- 20080227 snapshot
- fix build with gpac

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.0.0-0.11.20070819
- Merge freshrpms spec into livna spec for rpmfusion:
- Change version from 0 to 0.0.0 so that it is equal to the freshrpms versions,
  otherwise we would be older according to rpm version compare.
- Add Provides and Obsoletes x264-gtk to x264-gui for upgrade path from
  freshrpms
- Fix icon cache update scripts

* Sun Sep 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0-0.10.20070819
- Fix use of execstack on i386, closes livna bug #1659

* Sun Aug 19 2007 Dominik Mierzejewski <rpm@greysector.net> 0-0.9.20070819
- 20070819 snapshot, closes bug #1560

* Thu Nov 09 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.8.20061028
- use PIC on all platforms, fixes bug #1243

* Sun Oct 29 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.7.20061028
- fix desktop entry categories for devel

* Sun Oct 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.6.20061028
- fix BRs
- handle menu icon properly

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.5.20061028
- fix bad patch chunk
- fix 32bit build on x86_64

* Sat Oct 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.4.20061028
- Don't let ./configure to guess arch, pass it ourselves.
- Drop X-Livna desktop entry category.

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.3.20061028
- added GUI (based on kwizart's idea)
- latest snapshot
- added some docs to -devel

* Sun Oct 01 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.2.20061001
- add snapshot generator script
- fix make install
- make nasm/yasm BRs arch-dependent
- configure is not autoconf-based, call it directly

* Sat Sep 30 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.569
- Updated to latest SVN trunk
- specfile cleanups

* Mon Sep 04 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.558
- Updated to latest SVN trunk
- FE compliance

* Sun Mar 12 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.467
- Updated to latest SVN trunk
- Build shared library
- mp4 output requires gpac

* Mon Jan 02 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.394
- Updated to latest SVN trunk
- Change versioning scheme

* Sun Nov 27 2005 Dominik Mierzejewski <rpm@greysector.net> 0.0.375-1
- Updated to latest SVN trunk
- Added pkgconfig file to -devel

* Tue Oct  4 2005 Matthias Saou <http://freshrpms.net/> 0.0.315-1
- Update to svn 315.
- Disable vizualize since otherwise programs trying to link without -lX11 will
  fail (cinelerra in this particular case).

* Mon Aug 15 2005 Matthias Saou <http://freshrpms.net/> 0.0.285-1
- Update to svn 285.
- Add yasm build requirement (needed on x86_64).
- Replace X11 lib with lib/lib64 to fix x86_64 build.

* Tue Aug  2 2005 Matthias Saou <http://freshrpms.net/> 0.0.281-1
- Update to svn 281.

* Mon Jul 11 2005 Matthias Saou <http://freshrpms.net/> 0.0.273-1
- Initial RPM release.
