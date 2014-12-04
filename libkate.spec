Name:           libkate
Version:        0.4.1
Release:        2%{?dist}
Summary:        Libraries to handle the Kate bitstream format

Group:          System Environment/Libraries
License:        BSD
URL:            http://code.google.com/p/libkate/
Source0:        http://libkate.googlecode.com/files/libkate-%{version}.tar.gz

BuildRequires:  python-devel
BuildRequires:  libogg-devel
BuildRequires:  liboggz
BuildRequires:  libpng-devel
BuildRequires:  bison
BuildRequires:  flex
%ifarch %{ix86} x86_64 ppc ppc64 s390x %{arm}
BuildRequires:  valgrind
%endif
BuildRequires:  doxygen
 

%description
This is libkate, the reference implementation of a codec for the Kate bitstream
format.
Kate is a karaoke and text codec meant for encapsulation in an Ogg container.
It can carry text, images, and animate them.

Kate is meant to be used for karaoke alongside audio/video streams (typically
Vorbis and Theora), movie subtitles, song lyrics, and anything that needs text
data at arbitrary time intervals.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libogg-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package utils
Summary:        Encoder/Decoder utilities for %{name}
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Requires:       liboggz

%description utils
The %{name}-utils package contains the katedec/kateenc binaries for %{name}.

%package docs
Summary:        Documentation for %{name}
Group:          Documentation

BuildArch:      noarch

%description docs
The %{name}-docs package contains the docs for %{name}.


%prep
%setup -q

# We regenerate theses files at built step
rm tools/kate_parser.{c,h}
rm tools/kate_lexer.c


%build
%configure --disable-static

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Fix for header timestramps
touch -r $RPM_BUILD_ROOT%{_includedir}/kate/kate_config.h \
 $RPM_BUILD_ROOT%{_includedir}/kate/kate.h


%check
make check



%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%exclude %{_docdir}/libkate/html
%doc %{_docdir}/libkate
%{_libdir}/*.so.*

%files devel
%doc examples/
%{_includedir}/kate/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files utils
%{python_sitelib}/kdj/
%{_bindir}/KateDJ
%{_bindir}/katalyzer
%{_bindir}/katedec
%{_bindir}/kateenc
%{_mandir}/man1/KateDJ.*
%{_mandir}/man1/katalyzer.*
%{_mandir}/man1/katedec.*
%{_mandir}/man1/kateenc.*

%files docs
%doc %{_docdir}/libkate/html


%changelog
* Mon Aug 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.4.1-2
- Update to 0.4.1
- Spec file clean-up
- Set the current valgrind arches
- Use unversioned docdir - rhbz#993818

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.3.8-4
- Rebuild for new libpng

* Tue Mar 08 2011 Dennis Gilmore <dennis@ausil.us> - 0.3.8-3
- no valgrind on sparc or arm arches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.3.8-1
- Update to 0.3.8

* Sat Aug 28 2010 Dan Horák <dan[at]danny.cz> - 0.3.7-3
- no valgrind on s390(x)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Nov 25 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.3.7-1
- Update to 0.3.7

* Fri Oct 16 2009 kwizart < kwizart at gmail.com > - 0.3.6-1
- Update to 0.3.6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 kwizart < kwizart at gmail.com > - 0.3.4-1
- Update to 0.3.4

* Mon Jun 29 2009 kwizart < kwizart at gmail.com > - 0.3.3-2
- Split -docs - Fix #508589

* Mon May 11 2009 kwizart < kwizart at gmail.com > - 0.3.3-1
- Update to 0.3.3

* Fri Apr 10 2009 kwizart < kwizart at gmail.com > - 0.3.1-3
- Use Fedora compliant (using version) _docdir directory.
- Remove shebangs when not needed.
- Bundle examples within -devel
- Use global instead of define

* Sat Apr  4 2009 kwizart < kwizart at gmail.com > - 0.3.1-2
- Prevent conflict with GNU getline() in recent rawhide

* Tue Mar 17 2009 kwizart < kwizart at gmail.com > - 0.3.1-1
- Update to 0.3.1

* Tue Jan 13 2009 kwizart < kwizart at gmail.com > - 0.3.0-1
- Update to 0.3.0
- Add KateDJ and katalyzer in -utils
- Add BR liboggz and -utils Requires liboggz

* Wed Nov 27 2008 kwizart < kwizart at gmail.com > - 0.2.7-1
- Update to 0.2.7

* Mon Oct 20 2008 kwizart < kwizart at gmail.com > - 0.2.5-1
- Update to 0.2.5

* Mon Sep 29 2008 kwizart < kwizart at gmail.com > - 0.2.1-1
- Update to 0.2.1

* Thu Sep 11 2008 kwizart < kwizart at gmail.com > - 0.1.12-1
- Update to 0.1.12

* Thu Sep  4 2008 kwizart < kwizart at gmail.com > - 0.1.11-1
- Update to 0.1.11

* Wed Sep  3 2008 kwizart < kwizart at gmail.com > - 0.1.10-1
- Update to 0.1.10

* Tue Sep  2 2008 kwizart < kwizart at gmail.com > - 0.1.9-1
- Update to 0.1.9

* Fri Aug 29 2008 kwizart < kwizart at gmail.com > - 0.1.8-1
- Update to 0.1.8

* Mon Aug 11 2008 kwizart < kwizart at gmail.com > - 0.1.7-1
- Initial spec file

