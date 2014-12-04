Name:           vamp-plugin-sdk
Version:        2.5
Release:        2%{?dist}
Summary:        An API for audio analysis and feature extraction plugins

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.vamp-plugins.org/
Source0:        http://code.soundsoftware.ac.uk/attachments/download/690/vamp-plugin-sdk-2.5.tar.gz
# https://sourceforge.net/tracker/?func=detail&aid=1884043&group_id=192001&atid=939644
Patch0:         %{name}-2.5-libdir.patch

BuildRequires:  libsndfile-devel
#Requires:

%description
Vamp is an API for C and C++ plugins that process sampled audio data
to produce descriptive output (measurements or semantic observations).

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        static
Summary:        Static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description    static
The %{name}-static package contains library files for
developing static applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .libdir
sed -i 's|/lib/vamp|/%{_lib}/vamp|g' src/vamp-hostsdk/PluginHostAdapter.cpp
sed -i 's|/lib/|/%{_lib}/|g' src/vamp-hostsdk/PluginLoader.cpp


%build
%configure
make %{?_smp_mflags}


%install
# fix libdir
find . -name '*.pc.in' -exec sed -i 's|/lib|/%{_lib}|' {} ';'
make install DESTDIR=$RPM_BUILD_ROOT #INSTALL_PREFIX=%{_prefix} LIB=/%{_lib}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# create Makefile for examples
cd examples
echo CXXFLAGS=$RPM_OPT_FLAGS -fpic >> Makefile-%{_arch}
echo bundle: `ls *.o` >> Makefile
echo -e "\t"g++ \$\(CXXFLAGS\) -shared -Wl,-Bsymbolic \
     -o vamp-example-plugins.so \
     *.o \$\(pkg-config --libs vamp-sdk\) >> Makefile
echo `ls *.cpp`: >> Makefile
echo -e "\t"g++ \$\(CXXFLAGS\) -c $*.cpp >> Makefile
echo clean: >> Makefile
echo -e "\t"-rm *.o *.so >> Makefile
# clean directory up so we can package the sources
make clean


%check
# Scan shared libs for unpatched '/lib' strings to prevent issues
# on 64-bit multilib platforms.
[ $(strings ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.?|grep /lib|sed -e 's!/%{_lib}!/__FEDORA-LIB__!g'|grep -c /lib) -eq 0 ]


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/*.so.*
%{_libdir}/vamp

%files devel
%defattr(-,root,root,-)
%doc examples
%{_bindir}/vamp-*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Michel Salim <salimma@fedoraproject.org> - 2.5-1
- Update to 2.5

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep  9 2012 Michel Salim <salimma@fedoraproject.org> - 2.4-1
- Update to 2.4

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 14 2011 Michel Salim <salimma@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri May 28 2010 Michel Salim <salimma@fedoraproject.org> - 2.1-1
- Update to 2.1
- multilib fix: Makefile for examples is now arch-tagged

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0-5
- Add another sed libdir fix for PluginLoader.cpp (#469777)
  plus a check section to scan for libdir issues

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb  8 2009 Michel Salim <salimma@fedoraproject.org> - 2.0-3
- Fix compilation problem with GCC 4.4

* Tue Dec 30 2008 Michel Salim <salimma@fedoraproject.org> - 2.0-2
- More libdir fixes (bug #469777)

* Sun Dec 14 2008 Michel Salim <salimma@fedoraproject.org> - 2.0-1
- Update to 2.0

* Thu Jul 17 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.3-1
- Update to 1.3

* Thu Jan 31 2008 Michel Salim <michel.sylvan@gmail.com> - 1.1b-4
- Add some #includes, needed due to GCC 4.3's header dependency cleanup

* Mon Jan 28 2008 Michel Salim <michel.sylvan@gmail.com> - 1.1b-3
- Add examples to -devel subpackage
- Fix .pc files
- Preserve timestamps when installing

* Sun Jan 27 2008 Michel Salim <michel.sylvan@gmail.com> - 1.1b-2
- Add missing build requirement on libsndfile-devel

* Wed Jan 16 2008 Michel Salim <michel.sylvan@gmail.com> - 1.1b-1
- Initial Fedora package
