Name:          libmms
Version:       0.6.4
Release:       2%{?dist}
Summary:       Library for Microsoft Media Server (MMS) streaming protocol
License:       LGPLv2+
Group:         System Environment/Libraries
URL:           http://www.sf.net/projects/libmms
Source0:       http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch1:        0001-Remove-Requires-glib-2.0-since-libmms-no-longer-depe.patch

%description
MMS is a proprietary streaming protocol used in Microsoft server products,
commonly used to stream WMV data.  You can encounter mms:// style URLs all over
the net, especially on news sites and other content-serving sites. Libmms
allows you to download content from such sites, making it easy to add MMS
support to your media applications.


%package devel
Summary:       Development package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}, pkgconfig

%description devel
This package contains development files for %{name}.


%prep
%setup -q
%patch1 -p1


%build
export CFLAGS="$RPM_OPT_FLAGS -Wno-pointer-sign -Werror"
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags} 


%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/%{name}.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig 


%files
%doc AUTHORS COPYING.LIB ChangeLog README*
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sun Jun 15 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 0.6.4-2
- Add patch from upstream to drop glib requires from the pkg-config file
  (rhbz#1109495)

* Thu Apr 10 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 0.6.4-1
- New upstream bugfix release 0.6.4

* Sun Apr 06 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 0.6.3-1
- New upstream bugfix release 0.6.3

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.6.2-3
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan 19 2011 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6.2-1
- New upstream bugfix release 0.6.2

* Tue Jan 11 2011 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6.1-1
- New upstream bugfix release 0.6.1
- Fixes the use of the this reserved keyword in public headers (rf1596)

* Sun May 30 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6-1
- New upstream release 0.6
- Update URL (upstream has moved back to sf.net)

* Thu Feb 18 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.5-1
- New upstream release 0.5 (rf1053)
- Fix some regressions introduced by upstream
- Add a bunch of home grown patches (I used to be part of upstream, but
  upstream has moved to launchpad), fixing several bugs and cleaning up
  the code left and right, all these are submitted upstream

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.4-4
- rebuild for new F11 features

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-3
- Rebuild for buildsys cflags issue

* Wed Jul 23 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-2
- Release bump for rpmfusion build

* Fri Dec 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-1
- New upstream release 0.4
- Drop all patches (all upstreamed)

* Tue Dec 11 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-6
- Add a patch with various fixes from CVS
- Add a patch fixing a small bug I introduced in mmsh

* Sat Dec  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-5
- Add a patch from debian adding mms seeking support
- Add various fixes to Debians seeking patch
- Add self written mmsh seeking patch
- Add patch exporting some asf header info

* Wed Sep 12 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-4
- Add a patch from Debian fixing another crash
- Merge freshrpms spec into livna spec for rpmfusion:
- Set release to 4 to be higher as both livna and freshrpms latest release
- Update License tag for new Licensing Guidelines compliance
- Add pkgconfig Requires to -devel package
- Include some more doc files

* Wed Mar 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-3
- Add a patch fixing a crash (livna-bz 1463)

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.3-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.3-1
- New upstream release 0.3
- This new release fixes CVS-2006-2200

* Sun Sep 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-2
- Rebuild for FC-6

* Sat Jul 29 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2-1
- Minor specfile cleanups for livna submission.

* Mon Jun 12 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.2-0.gst.2
- new release

* Wed Jan 05 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.1-0.gst.1
- initial package
