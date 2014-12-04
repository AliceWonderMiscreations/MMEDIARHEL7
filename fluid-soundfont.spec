Name:           fluid-soundfont
Version:        3.1
Release:        11%{?dist}
Summary:        Pro-quality GM/GS soundfont
Group:          Applications/Multimedia
License:        MIT
# The original URL (http://www.powermage.com/fluid) seems dead. Therefore we point
# to the Hammersound archives:
URL:            http://www.hammersound.com/cgi-bin/soundlink.pl?action=view_category&category=Collections&ListStart=0&ListLength=20
# The Hammersound source gives us a soundfont in a linux-unfriendly .sfArk format. 
# In order to convert this to a linux-friendly .sf2 format one needs to use a 
# non-free utility sfarkxtc from 
#    http://www.melodymachine.com
# This page explains how this conversion is done:
#    http://vsr.informatik.tu-chemnitz.de/staff/jan/nted/doc/ch01s46.html
# Debian folks already did this and we will borrow their source tarball:
Source0:        http://ftp.de.debian.org/debian/pool/main/f/%{name}/%{name}_%{version}.orig.tar.gz
# Some information about the soundfont that can be found in the Hammersound archive:
Source1:        Fluid_R3_Readme.pdf
# Optimized cfg files for fluid usage with timidity, written by Saito, one of
# the TiMidity++ developers
Source2:        timidity++.cfg
Source3:        fluid3gm.cfg
Source4:        fluid3gs.cfg
Source5:        fluid_altassign.cfg
BuildArch:      noarch
BuildRequires:  soundfont-utils


%define common_description \
FluidR3 is the third release of Frank Wen's pro-quality GM/GS soundfont.\
The soundfont has lots of excellent samples, including all the GM instruments\
along side with the GS instruments that are recycled and reprogrammed versions\
of the GM presets.

%description
%common_description

%package common
Summary:        Common files for FluidR3 soundfont
Group:          Applications/Multimedia

%description common
%common_description

This package contains common files shared among all FluidR3 soundfont packages.

%package gm
Summary:        Pro-quality General Midi soundfont
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Provides:       soundfont2
Provides:       soundfont2-default
# If timidity++ is installed it must understand the trysouce configfile keyword
Conflicts:      timidity++ <= 2.13.2-30.cvs20111110%{?dist}

%description gm
%common_description

This package contains Fluid General Midi (GM) soundfont in soundfont 2.0 (.sf2)
format.

%package gs
Summary:        Pro-quality General Standard Extension soundfont
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       %{name}-gm = %{version}-%{release}
Provides:       soundfont2


%description gs
%common_description

This package contains instruments belonging to General Midi's General Standard
(GS) Extension in soundfont 2.0 (.sf2) format.

%package lite-patches
Summary:        Pro-quality General Midi soundfont in GUS patch format
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Provides:       timidity++-patches = 5
Obsoletes:      timidity++-patches < 5
Obsoletes:      PersonalCopy-Lite-patches < 5

%description lite-patches
%common_description

This package contains Fluid General Midi (GM) soundfont in Gravis Ultrasound
(GUS) patch (.pat) format.


%prep
%setup -q
cp -a %{SOURCE1} .

%build
unsf -v -s -m FluidR3_GM.sf2
unsf -v -s -m FluidR3_GS.sf2

# Cut the size of the patches subpackage:
for bank in GM-B{8,9,16} Standard{1,2,3,4,5,6,7} Room{1,2,3,4,5,6,7} Power{1,2,3} Jazz{1,2,3,4} Brush{1,2}; do
   sed -i "/$bank/d" FluidR3_GM.cfg
   rm -fr *$bank*
done

cat FluidR3_GM.cfg FluidR3_GS.cfg > FluidR3.cfg

# The gus patches get used by a lot of different programs and some need the
# path to the patches to be absolute
sed -i 's|FluidR3_GM-|%{_datadir}/soundfonts/%{name}-lite-patches/FluidR3_GM-|g' FluidR3.cfg
sed -i 's|FluidR3_GS-|%{_datadir}/soundfonts/%{name}-lite-patches/FluidR3_GS-|g' FluidR3.cfg

%install
# The actual soundfonts:
mkdir -p $RPM_BUILD_ROOT%{_datadir}/soundfonts
install -p -m 644 FluidR3_GM.sf2 $RPM_BUILD_ROOT%{_datadir}/soundfonts
install -p -m 644 FluidR3_GS.sf2 $RPM_BUILD_ROOT%{_datadir}/soundfonts
# Create a symlink to denote that this is the Fedora default soundfont
ln -s FluidR3_GM.sf2 $RPM_BUILD_ROOT%{_datadir}/soundfonts/default.sf2

# timidity++.cfg files for usage of the sf2 files with the real timidity
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 644 %{SOURCE3} %{SOURCE4} %{SOURCE5} \
    $RPM_BUILD_ROOT%{_datadir}/soundfonts

# Gus patches + timidity.cfg, for programs which want the "old" timidity.cfg
mkdir -p $RPM_BUILD_ROOT%{_datadir}/soundfonts/%{name}-lite-patches
cp -a FluidR3_GM-* $RPM_BUILD_ROOT%{_datadir}/soundfonts/%{name}-lite-patches
cp -a FluidR3_GS-* $RPM_BUILD_ROOT%{_datadir}/soundfonts/%{name}-lite-patches
install -p -m 644 FluidR3.cfg $RPM_BUILD_ROOT%{_sysconfdir}/timidity.cfg


%files common
%doc COPYING README *Readme*
%dir %{_datadir}/soundfonts/

%files gm
%{_sysconfdir}/timidity++.cfg
%{_datadir}/soundfonts/FluidR3_GM.sf2
%{_datadir}/soundfonts/default.sf2
%{_datadir}/soundfonts/fluid3gm.cfg
%{_datadir}/soundfonts/fluid_altassign.cfg

%files gs
%{_datadir}/soundfonts/FluidR3_GS.sf2
%{_datadir}/soundfonts/fluid3gs.cfg

%files lite-patches
%config %{_sysconfdir}/timidity.cfg
%{_datadir}/soundfonts/%{name}-lite-patches/


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Hans de Goede <hdegoede@redhat.com> - 3.1-8
- Use trysource for the gs config in timidity++.cfg (rhbz#815611)

* Sat Jan 21 2012 Hans de Goede <hdegoede@redhat.com> - 3.1-7
- Add timidity++.cfg files tweaked for using FluidR3 with timidity++, written
  by Saito, one of the TiMidity++ developers

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 3.1-3
- Add real (non-virtual) Obsoletes: PersonalCopy-Lite-patches < 5

* Mon Mar 23 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 3.1-2
- Build lite-patches package by default (remove conditionals)
- Include only mono banks in the lite-patches package
- Create a symlink default.sf2 pointing to FluidR3_GM.sf2
- Add "Provides: soundfont2" to gm and gs packages
- Add "Provides: soundfont2-default" to gm package
- Add "Obsoletes/Provides: timidity++-patches (<)= 5" to the lite-patches package
- Add common subpackage for directory ownership and the doc files
- Update descriptions

* Sun Feb 01 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 3.1-1.2
- Attempt to cut down the size of the (lite-)patches subpackage by extracting only
  a single layer for each instrument and by removing some banks

* Sat Jan 31 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 3.1-1.1
- Mockup for optional GUS-patches subpackages (disabled by default)

* Fri Jan 30 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 3.1-1
- Initial Fedora build. SPEC file adapted from PersonalCopy-Lite-soundfont
