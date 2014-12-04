%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           zbar
Version:        0.10
Release:        19%{?dist}
Summary:        Bar code reader

Group:          User Interface/X Hardware Support
License:        LGPLv2+
URL:            http://zbar.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		zbar_update_to_hg.patch
Patch1:		zbar_use_libv4l.patch
Patch2:		zbar_choose_supported_format_first.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
 
BuildRequires:	autoconf automake libtool python-devel gettext-devel
BuildRequires:	qt4-devel gtk2-devel pygtk2-devel GraphicsMagick-c++-devel
BuildRequires:	libv4l-devel libXv-devel xmlto

%description
A layered barcode scanning and decoding library. Supports EAN, UPC, Code 128,
Code 39 and Interleaved 2 of 5.
Includes applications for decoding captured barcode images and using a video 
device (eg, webcam) as a barcode scanner.

%package devel
Group: Development/Libraries
Summary: Bar code library extra development files
Requires: pkgconfig, %{name} = %{version}-%{release}

%description devel
This package contains header files and additional libraries used for
developing applications that read bar codes with this library.

%package gtk
Group: Development/Libraries
Summary: Bar code reader GTK widget
Requires: %{name} = %{version}-%{release}

%description gtk
This package contains a bar code scanning widget for use with GUI
applications based on GTK+-2.0.

%package gtk-devel
Group: Development/Libraries
Summary: Bar code reader GTK widget extra development files
Requires: pkgconfig, %{name}-gtk = %{version}-%{release}, %{name}-devel = %{version}-%{release}

%description gtk-devel
This package contains header files and additional libraries used for
developing GUI applications based on GTK+-2.0 that include a bar code
scanning widget.

%package pygtk
Group: Development/Libraries
Summary: Bar code reader PyGTK widget
Requires: pygtk2, %{name}-gtk = %{version}-%{release}

%description pygtk
This package contains a bar code scanning widget for use in GUI
applications based on PyGTK.

%package qt
Group: Development/Libraries
Summary: Bar code reader Qt widget
Requires: %{name} = %{version}-%{release}

%description qt
This package contains a bar code scanning widget for use with GUI
applications based on Qt4.

%package qt-devel
Group: Development/Libraries
Summary: Bar code reader Qt widget extra development files
Requires: pkgconfig, %{name}-qt = %{version}-%{release}, %{name}-devel = %{version}-%{release}

%description qt-devel
This package contains header files and additional libraries used for
developing GUI applications based on Qt4 that include a bar code
scanning widget.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
autoreconf -vfi
%configure --with-graphicsmagick --docdir=%{_docdir}/%{name}-%{version}

# rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

#Remove .la and .a files
find ${RPM_BUILD_ROOT} -name '*.la' -or -name '*.a' | xargs rm -f

# Remove installed doc
rm -rf $RPM_BUILD_ROOT/usr/share/doc/zbar-0.10/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post devel -p /sbin/ldconfig

%post gtk -p /sbin/ldconfig

%post qt -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%postun gtk -p /sbin/ldconfig

%postun qt -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING LICENSE NEWS

%{_bindir}/zbarimg
%{_bindir}/zbarcam
%{_libdir}/libzbar.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc HACKING TODO

%{_libdir}/libzbar.so
%{_libdir}/pkgconfig/zbar.pc
%dir %{_includedir}/zbar
%{_includedir}/zbar.h
%{_includedir}/zbar/Exception.h
%{_includedir}/zbar/Symbol.h
%{_includedir}/zbar/Image.h
%{_includedir}/zbar/Scanner.h
%{_includedir}/zbar/Decoder.h
%{_includedir}/zbar/ImageScanner.h
%{_includedir}/zbar/Video.h
%{_includedir}/zbar/Window.h
%{_includedir}/zbar/Processor.h

%files gtk
%defattr(-,root,root,-)
%{_libdir}/libzbargtk.so.*

%files gtk-devel
%defattr(-,root,root,-)
%{_libdir}/libzbargtk.so
%{_libdir}/pkgconfig/zbar-gtk.pc
%{_includedir}/zbar/zbargtk.h

%files pygtk
%defattr(-,root,root,-)
%{python_sitearch}/zbarpygtk.so
%{python_sitearch}/zbar.so

%files qt
%defattr(-,root,root,-)
%{_libdir}/libzbarqt.so.*

%files qt-devel
%defattr(-,root,root,-)
%{_libdir}/libzbarqt.so
%{_libdir}/pkgconfig/zbar-qt.pc
%{_includedir}/zbar/QZBar*.h

%changelog
* Tue Aug 06 2013 Mauro Carvalho Chehab <m.chehab@samsung.com> - 0.10-19
- Fix Fedora 20 build problems

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.10-17
- Rebuild.

* Fri Feb 22 2013 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.10-16
- Change zbar to use GraphicsMagick instead of ImageMagick

* Fri Feb 22 2013 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.10-15
- zbar 0.10 source generated via hg archive -r 0.10 ../zbar-0.10.tar.bz2
  That allows to better handle the difference from 0.10 to -hg
- Update to the latest hg patch

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.10-13
- rebuild against new libjpeg

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 01 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.10-11
- Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.10-9
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 25 2010 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.10-7
- Prefer to use non-emulated formats

* Sun Dec 05 2010 Mauro Carvalho Chehab <mchehab@redhat.com>
- Update it to the newest version available at zbar git directory
- Use libv4l to communicate with video devices

* Wed Sep 29 2010 jkeating - 0.10-5
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Hans de Goede <hdegoede@redhat.com> 0.10-4
- Rebuild for new ImageMagick

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Nov 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.10-2
- Rebuild for Qt 4.6.0 RC1 in F13 (was built against Beta 1 with unstable ABI)
- Always BR qt4-devel rather than qt-devel, it's provided by qt-devel anyway

* Mon Nov 02 2009 Bastien Nocera <bnocera@redhat.com> 0.10-1
- Update to 0.10

* Wed Jul 29 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-7
- Replace URL info

* Wed Jul 29 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.8-6
- fix epel build

* Tue Jul 28 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-5
- Now fixed Source0 url
- Removed ldconfig calls to devel subpackages
- Fixed directory ownership issue -pygtk
- Added %%{name} to URL
- Added comment to rpath 
- Improved comment for removing .la and .a files

* Mon Jul 27 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-4
- Fixed sourceforge url
- Removed redundant libX11-devel package from BuildRequires
- Removed redundant ImageMagick package from Requires
- Removed Provides for not included static libs
- Removed redundant requires to subpackages -qt and -gtk
- Removed redundant {name} = %%{version}-%%{release} from -pygtk
- Replaced macros from % to %% in changelog 
- Fixed ownership issue
- Added ldconfig call to devel, qt-devel and gtk-devel

* Fri Jul 24 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-3
- Fixed License from LGPLv2 to LGPLv2+
- Added to main BuildRequires libXv-devel and xmlto packages
- Removed pkgconfig from main BuildRequires
- Removed .la and .a files
- Removed version validation from ImageMagick-c++ and ImageMagick-c++-devel packages
- Replaced 3 {%%version} to %%{version} (packages: devel, qt-devel, gtk-devel)
- Removed duplicated description for each package
- Added %%{version}-%%{release} to packages: devel, gtk, gtk-devel, pygtk, qt
- Added pkgconfig to packages gtk-devel, qt-devel into Requires session
- Removed redundant packages
- Added dependency of gtk to pygtk
- Added timestamp on installed files
- Replaced %%{_datadir}/man to %%{_mandir}
- Removed INSTALL file
- Fixed %%doc session
- Added to -devel own of %%{_includedir}/zbar directory
- Replaced "%%{_libdir}/python*" to %%{python_sitearch}
- Fixed %%defattr
- Fixed Release Number and Changelog
- Fixed rpath error

* Thu Jul 16 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-2
- Added pkgconfig to devel package 
- Fixed syntax to ldconfig 
- Fixed warnings from rpmlint
- Fixed static path to docs

* Wed Jul 15 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-1
- First release, based on original zbar.spec provided by sources
