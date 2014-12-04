Name:		awel-gstreamer-release
Version:	7
Release:	2
Summary:	Custom GStreamer Packages for RHEL/CentOS 7

Group:		System Environment/Base 
License:	Public Domain

URL:		http://awel.domblogger.net/
Source0:	awel-gstreamer.repo

BuildArch:	noarch
Requires:	awel-release >= %{version}	

%description
This package contains the the yum configuration information and the public GPG
key used with the RPM packages for RHEL/CentOS 7 built by Alice Wonder.

This repository contains custom GStreamer packages that will REPLACE the
GStreamer packages provided in RHEL/CentOS 7. As such you should not use this
package repository unless you KNOW you need the newer GStreamer (e.g. to get
support for VP9 decoding)

After installing this package, a yum update will replace the distribution
GStreamer1 packages with the packages provided here.

This package repository has dependencies from the awel-media repository.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .

%build


%install
rm -rf %{buildroot}

# yum
install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config /etc/yum.repos.d/*

%changelog
* Sat Oct 18 2014 Alice Wonder <rpmbuild@domblogger.net> - 7-2
- Don't make yum repo for debug packages

* Fri Sep 26 2014 Alice Wonder <rpmbuild@domblogger.net> - 7-1
- Initial release
