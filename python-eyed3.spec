Name:           python-eyed3
Version:        0.7.5
Release:        1%{?dist}
Summary:        Python audio data toolkit (ID3 and MP3)
License:        GPLv2+
URL:            http://eyed3.nicfit.net/
Source0:        http://eyed3.nicfit.net/releases/eyeD3-%{version}.tgz
Patch0:		eyeD3-lameinfo.patch
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python-setuptools
Requires:       python-magic

%description
A Python module and program for processing ID3 tags. Information about
mp3 files(i.e bit rate, sample frequency, play time, etc.) is also
provided. The formats supported are ID3 v1.0/v1.1 and v2.3/v2.4.

%prep
%setup -qn eyeD3-%{version}
%patch0 -p1

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%check
%{__python2} setup.py test

%files
%doc AUTHORS ChangeLog COPYING README.rst examples/
%{_bindir}/eyeD3
%{python2_sitelib}/eyed3/
%{python2_sitelib}/eyeD3-%{version}-py%{python2_version}.egg-info/

%changelog
* Thu Oct 09 2014 Alice Wonder <rpmbuild@domblogger.net> - 0.7.5-1
- Fixed missing import math in lameinfo.py
- Update to 0.7.5

* Fri Jan 10 2014 Christopher Meng <rpm@cicku.me> - 0.7.4-2
- Dependencies cleanup.

* Fri Dec 27 2013 Christopher Meng <rpm@cicku.me> - 0.7.4-1
- Update to 0.7.4.
- Add EPEL support.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Christopher Meng <rpm@cicku.me> - 0.7.3-1
- New version.
- Remove paver BR.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 bpepple <bpepple@fedoraproject.org> 0.6.18-2
- Rebase UserTextFrames patch.

* Fri Jan 27 2012 bpepple <bpepple@fedoraproject.org> 0.6.18-1
- Update to 0.6.18.

* Mon Jan 09 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.6.17-7
- Rebuild for new gcc.

* Fri Aug  5 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.6.17-6
- Add patch to fix crashes on files with empty UserTextFrames.
- Drop buildroot & clean sections. No longer needed.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.17-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  3 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.6.17-1
- Update to 0.6.17.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.16-2
- Rebuild for Python 2.6

* Thu Jun 19 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.16-1
- Update to 0.6.16.

* Sat Mar  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.6.15-1
- Update to 0.6.15.
- Update license tag.

* Fri May 18 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.6.14-1
- Update to 0.6.14.

* Sat Feb 24 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.6.12-1
- Update to 0.6.12.

* Fri Dec  8 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.6.11-3
- Change BR to python-devel.

* Fri Dec  8 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.6.11-2
- Rebuild against new python.

* Wed Nov 22 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.6.11-1
- Update to 0.6.11.

* Sat Oct  7 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.6.10-2
- Change BR to python.
- Remove unnecessary make in build section.

* Sat Oct  7 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.6.10-1
- Initial FE spec.
