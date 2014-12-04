Name:		libdvdcss
Version:	1.3.0
Release:	1%{?dist}
Summary:	A library designed for accessing DVDs like a block device

Group:		System Environment/Libraries
License:	GPLv2
URL:		http://www.videolan.org/developers/libdvdcss.html
Source0:	http://download.videolan.org/pub/libdvdcss/1.3.0/%{name}-%{version}.tar.bz2

#BuildRequires:	gtk-doc
BuildRequires:	doxygen
#Requires:	

%description
libdvcss is a simple library designed for accessing DVDs like a block device
without having to bother about the decryption

%package devel
Summary:	Developer header files and documentation
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package includes the header file and developer documentation needed to
compile software that links against %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
mv %{buildroot}%{_datadir}/doc/libdvdcss ./developer-doc

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README NEWS AUTHORS
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc developer-doc/*
%{_includedir}/dvdcss
%{_libdir}/libdvdcss.so
%{_libdir}/pkgconfig/libdvdcss.pc



%changelog
* Thu Oct 02 2014 Alice Wonder <alicewonder@shastaherps.org> - 1.3.0-1
- Initial spec file for AWEL
