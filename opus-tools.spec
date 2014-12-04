Name:          opus-tools
Version:       0.1.7
Release:       1%{?dist}
Summary:       A set of tools for the opus audio codec

Group:         System Environment/Libraries
License:       BSD and GPLv2
URL:           http://www.opus-codec.org/
Source0:       http://downloads.xiph.org/releases/opus/%{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: flac-devel
BuildRequires: libogg-devel
BuildRequires: opus-devel

%description
The Opus codec is designed for interactive speech and audio transmission over 
the Internet. It is designed by the IETF Codec Working Group and incorporates 
technology from Skype's SILK codec and Xiph.Org's CELT codec.

This is a set of tools for the opus codec.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%check
make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_bindir}/opus*
%{_datadir}/man/man1/opus*

%changelog
* Mon Sep  9 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.7-1
- update to 0.1.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.6-1
- update to 0.1.6

* Tue Sep  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.5-1
- update to 0.1.5

* Thu Aug  2 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.4-1
- update to 0.1.4

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.3-1
- update to 0.1.3

* Thu Jun 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.2-1
- Initial packaging
