Name:       nas 
Summary:    The Network Audio System (NAS)
Version:    1.9.4
Release:    1%{?dist}
URL:        http://radscan.com/nas.html
# README:               MIT (main license)
# config/aclocal.m4:    FSFULLR
# config/config.sub:    GPL with exceptions, effectively same as main license
# config/ltmain.sh:     GPLv2+ with exceptions, effectively same as main license
# config/config.guess:  GPLv2+ with exceptions, effectively same as main license
# config/configure:     FSFUL
# config/install-sh:    MIT
# server/dda/voxware/auvoxware.h:
#                           (MIT) and
#                           (something similar to MIT license by SCO)
# server/dda/sun/ausuni.c:  (MIT) and
#                           (something similar to MIT)
# lib/audio/aiff.c          MIT (with Apple warranty declaration)
# Following flawed files has been removed or correcterd according to upstream
# commit e43cf3377b8b87114796556f5ad0469d4e79e183:
# server/dda/hpux/auhpux.h: (MIT) and
#                           (as-is with unclear commercial prohibition)
# doc/xcon94slide.ps:       All rights reserved (Frame Technology Corporation)
# doc/overview.ps:          All rights reserved (Network Computing Devices)
# doc/library.ps:           All rights reserved (Network Computing Devices)
# doc/title.ps:             All rights reserved (Network Computing Devices)
License:    MIT
Group:      Development/Libraries
%define daemon nasd
# Original source nas-1.9.4.src.tar.gz (MD5:dac0e6cd3e5d6a37ae1dff364236a752)
# is from
# <http://downloads.sourceforge.net/%%{name}/%%{name}-%%{version}.src.tar.gz>.
# The nas-1.9.4.repacked.tar.gz corrects flawed files according to upstream
# commit e43cf3377b8b87114796556f5ad0469d4e79e183. Offical post-1.9.4 release
# should be free as speech and will not need repacking.
Source0:    %{name}-%{version}.repacked.tar.gz
Source1:    %{daemon}.service
Source2:    %{daemon}.sysconfig
Patch0:     %{name}-1.9.3-Move-AuErrorDB-to-SHAREDIR.patch
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  imake
BuildRequires:  libX11-devel
BuildRequires:  libXau-devel
BuildRequires:  libXaw-devel
BuildRequires:  libXext-devel
BuildRequires:  libXp-devel
BuildRequires:  libXt-devel
BuildRequires:  systemd-units
# Update config.sub to support aarch64, bug #926196
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
Requires:           %{name}-libs = %{version}-%{release}
Requires(post):     systemd-sysv systemd-units
Requires(preun):    systemd-units
Requires(postun):   systemd-units


%package devel
Summary:    Development and doc files for the NAS 
Group:      Development/Libraries
Requires:   %{name}-libs = %{version}-%{release}

%package libs
Summary:    Run-time libraries for NAS
Group:      System Environment/Libraries


%description
In a nutshell, NAS is the audio equivalent of an X display server.  The
Network Audio System (NAS) was developed for playing, recording, and
manipulating audio data over a network.  Like the X Window System, it uses the
client/server model to separate applications from the specific drivers that
control audio input and output devices.

Key features of the Network Audio System include:
    • Device-independent audio over the network
    • Lots of audio file and data formats
    • Can store sounds in server for rapid replay
    • Extensive mixing, separating, and manipulation of audio data
    • Simultaneous use of audio devices by multiple applications
    • Use by a growing number of ISVs
    • Small size
    • Free!  No obnoxious licensing terms

%description libs
%{summary}.

%description devel
Development files and the documentation for Network Audio System.


%prep
%setup -q
%patch0 -p1 -b .move_AuErrorDB

# Update config.sub to support aarch64, bug #926196
cp -p %{_datadir}/automake-*/config.{sub,guess} config
sed -i -e '/AC_FUNC_SNPRINTF/d' config/configure.ac
autoreconf -i -f config
for F in HISTORY; do
    iconv --from-code=ISO_8859-15 --to-code=UTF-8 "$F" > "${F}.tmp"
    touch -r "$F" "${F}.tmp"
    mv "${F}.tmp" "$F"
done


%build
xmkmf
# See HISTORY file how to modify CDEBUGFLAGS
make WORLDOPTS='-k CDEBUGFLAGS="%{optflags}"' %{?_smp_mflags} World


%install
make DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} INCROOT=%{_includedir} \
  LIBDIR=%{_libdir}/X11  SHLIBDIR=%{_libdir} USRLIBDIR=%{_libdir} \
  MANPATH=%{_mandir} INSTALLFLAGS='-p' \
  install install.man

install -p -m644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/%{daemon}.service
install -p -m644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{daemon}

# Remove static libraries
rm $RPM_BUILD_ROOT%{_libdir}/*.a
# Rename config file
mv $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/nasd.conf{.eg,}


%post
%systemd_post %{daemon}.service

%preun
%systemd_preun %{daemon}.service

%postun
%systemd_postun_with_restart %{daemon}.service

%triggerun -- %{name} < 1.9.3-1
echo '%{name}: User must migrate to systemd target manually by runnig:'
echo '  systemd-sysv-convert --apply %{daemon}'
# Save the current service runlevel info
/usr/bin/systemd-sysv-convert --save %{daemon} >/dev/null 2>&1 ||:
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del %{daemon} >/dev/null 2>&1 || :
/bin/systemctl try-restart %{daemon}.service >/dev/null 2>&1 || :



%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/nasd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{daemon}
%{_unitdir}/%{daemon}.service
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files libs
# The LICENSE_CLARIFICIATION is specific to repacked sources.
%doc FAQ HISTORY LICENSE_CLARIFICIATION README TODO
%{_libdir}/libaudio.so.*
%{_datadir}/X11/AuErrorDB

%files devel
%doc doc/actions doc/protocol.txt doc/*.ps
%{_includedir}/audio/
%{_libdir}/libaudio.so
%{_mandir}/man3/*


%changelog
* Tue Oct 08 2013 Petr Pisar <ppisar@redhat.com> - 1.9.4-1
- 1.9.4 bump
- Package license corrected to MIT

* Mon Sep 16 2013 Petr Pisar <ppisar@redhat.com> - 1.9.3-9
- Fix CVE-2013-4258 (formatting string for syslog call) (bug #1006753)
- Fix CVE-2013-4256 (parsing display number) (bug #1006753)
- Fix CVE-2013-4257 (heap overflow when processing AUDIOHOST variable)
  (bug #1006753)
- Fix race when opening a TCP device (bug #1006753)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.9.3-7
- Perl 5.18 rebuild

* Wed Mar 27 2013 Petr Pisar <ppisar@redhat.com> - 1.9.3-6
- Update config.sub to support aarch64 (bug #926196)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 1.9.3-4
- Modernize systemd scriptlets

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 02 2011 Petr Pisar <ppisar@redhat.com> - 1.9.3-1
- 1.9.3 bump
- Remove useless spec code
- Migrate nasd service from sysvinit to systemd

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 09 2010 Petr Pisar <ppisar@redhat.com> - 1.9.2-1
- 1.9.2 bump, update URL, Source0
- Remove spec code specific for Fedora < 12 and EPEL < 4 as they are
  unsupported now
- Apply nas-1.9.2-asneeded.patch to get libXau linked explicitly (bug #565181)
- Move AuErrorDB non-executable to share directory, distribute with libraries
- Unify spec file indentation
- Add postun action

* Sun Mar 14 2010 Frank Büttner <frank-buettner@gmx.net> - 1.9.1-7
- fix #565181

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Apr 07 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.9.1-4
- -libs subpkg (f9+, #438547)
- %%install: INSTALLFLAGS='-p' (preserve timestamps)
- fixup %%changelog whitespace

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.9.1-3
- Autorebuild for GCC 4.3

* Sun Nov 11 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9.1-2
- fix spec file

* Sun Nov 11 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9.1-1
- update to 1.9.1
- remove unneeded patches

* Fri Nov 02 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9a-3
- add better patch for #247468 

* Fri Nov 02 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9a-2
- add patch to fix #247468

* Sun Oct 28 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9a-1
- update to 1.9a to fix #245712

* Sat Aug 18 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9-4
- fix for bug #245712

* Sat Aug 11  2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9-3
- fix for bug #250453

* Fri May 04 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9-2%{?dist}
- rebuild for the new ppc64 arch

* Sun Apr 08 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.9-1%{?dist}
- update to 1.9
- remove old patch file

* Mon Mar 26 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8b-1%{?dist}
- update to 1.8b

* Thu Mar 22 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8a-2%{?dist}
- use the SVN version of 1.8a

* Wed Mar 21 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8a-1%{?dist}
- fix bug 233353 

* Fri Feb 09 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8-13%{?dist}
- use the corrected patch

* Thu Feb 08 2007 Frank Büttner  <frank-buettner@gmx.net> - 1.8-11%{?dist}
- fix bug 227759

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.8-10
- don't rely-on/use potentially broken %%_libdir/X11 symlink (#207180)

* Mon Sep 11 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-9%{?dist}
- second rebuild for FC6

* Mon Jul 24 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-8%{?dist}
- fix ugly output when starting the daemon

* Fri Jul 21 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-7%{?dist}
- disable build for EMT64 on FC4

* Thu Jul 13 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-6%{?dist}
- fix build on EMT64 

* Wed Jul 12 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-5%{?dist}
- fix include dir

* Fri Jul 7 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-4%{?dist}
- add Requires(preun): chkconfig /sbin/service
- add Requires(post):  chkconfig
- add remarks for FC4

* Fri Jul 7 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-3%{?dist}
- move man3 to devel
- rename nasd.conf.eg to .conf
- add build depend for libXext-devel libXt-devel
- change license to Public Domain
- add path to make intall
- add rc.d/sysconfig  files 

* Fri Jul 7 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-2%{?dist}
- move libaudio.so.2 to main package
- switch package name from NAS to nas
- fix depend for devel package
- fix version
- add nas subdir in etc to main package
- set license to Distributable
- add readme file

* Fri Jul 7 2006 Frank Büttner  <frank-buettner@gmx.net> - 1.8-1%{?dist}
- start
