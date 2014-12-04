Name:           libmodplug
Version:        0.8.8.5
Release:        1%{?dist}
Epoch:          1
Summary:        Modplug mod music file format library

Group:          System Environment/Libraries
License:        Public Domain
URL:            http://modplug-xmms.sourceforge.net/
Source0:        http://downloads.sourceforge.net/modplug-xmms/%{name}-%{version}.tar.gz
# Fedora specific, no need to send upstream
Patch0:         %{name}-0.8.4-timiditypaths.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
%{summary}.

%package        devel
Summary:        Development files for the Modplug mod music file format library
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description    devel
%{summary}.


%prep
%setup -q
%patch0 -p1
sed -i -e 's/\r//g' ChangeLog


%build
%configure
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_libdir}/libmodplug.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libmodplug/
%{_libdir}/libmodplug.so
%{_libdir}/pkgconfig/libmodplug.pc


%changelog
* Mon Mar 10 2014 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.8.5-1
- Update to 0.8.8.5 (CVE-2013-4233, CVE-2013-4234, #995580).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug  7 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.8.4-1
- Update to 0.8.8.4 (security, #728371).

* Tue May 10 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.8.3-3
- Drop dependency on /etc/timidity.cfg, it's not worth the 100MB+ it pulls in.

* Mon May  9 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.8.3-2
- Don't require /etc/timidity.cfg on EL-6, there is no suitable provider
  package available in it at the moment.

* Sun May  8 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.8.3-1
- Update to 0.8.8.3 (security, CVE-2011-1761).
- Require /etc/timidity.cfg for ABC and MIDI.

* Sat Apr  2 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.8.2-1
- Update to 0.8.8.2 (security, CVE-2011-1574).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 21 2010 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.8.1-2
- Make -devel main package dependency ISA qualified.

* Wed Apr  7 2010 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.8.1-1
- Update to 0.8.8.1 (#580021).
- Drop explicit pkgconfig dependency from -devel (autodetected in F-12+).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 27 2009 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.7-1
- Update to 0.8.7 (security, #496834).

* Tue Apr 14 2009 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.5-1
- Update to 0.8.5, should fix #483146.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  9 2008 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.4-3
- Rebuild.

* Tue Aug 21 2007 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.4-2
- Rebuild.

* Wed Apr  4 2007 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8.4-1
- 0.8.4.

* Tue Oct  3 2006 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8-3
- Apply patch for CVE-2006-4192 (from Debian).

* Mon Aug 28 2006 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8-2
- Rebuild.

* Fri Mar 24 2006 Ville Skyttä <ville.skytta@iki.fi> - 1:0.8-1
- 0.8, 64bit patch included upstream.

* Mon Feb 13 2006 Ville Skyttä <ville.skytta@iki.fi> - 1:0.7-5
- Rebuild, cosmetics.

* Tue Aug 23 2005 Ville Skyttä <ville.skytta@iki.fi> - 1:0.7-4
- Don't ship static libs.

* Tue Aug 23 2005 Ville Skyttä <ville.skytta@iki.fi> - 1:0.7-3
- Fix x86_64, thanks to Adam Goode (#166127).

* Thu Mar 17 2005 Ville Skyttä <ville.skytta@iki.fi> - 1:0.7-2
- Build with dependency tracking disabled.
- Run tests in the %%check section.

* Fri Oct 17 2003 Ville Skyttä <ville.skytta@iki.fi> - 1:0.7-0.fdr.1
- First build, separated from xmms-modplug.
- Bump Epoch.
