%global __cmake_in_source_build 1

%global commit0 bbe30e300c1618207f447927b0accedd51ab8769
%global date 20201102
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

Name:           dhewm3
Version:        1.5.1
Release:        10%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Dhewm's Doom 3 engine
License:        GPLv3+ with exceptions
URL:            https://dhewm3.org/

%if 0%{?tag:1}
Source0:        https://github.com/dhewm/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Source0:        https://github.com/dhewm/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

Source1:        %{name}-README.txt
Patch0:         %{name}-no-cdkey.patch

ExcludeArch:    ppc64le

# Generic provider for Doom 3 engine based games
Provides:       doom3-engine = 1.3.1.1304

Provides:       bundled(minizip-idsoftware) = 1.2.7

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libcurl-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  openal-soft-devel
BuildRequires:  SDL2-devel
BuildRequires:  speex-devel
BuildRequires:  zlib-devel

%description
%{name} 3 is a Doom 3 GPL source modification. The goal of %{name} 3 is bring
DOOM 3 with the help of SDL to all suitable platforms. Bugs present in the
original DOOM 3 will be fixed (when identified) without altering the original
game-play.

%prep
%autosetup -p1 -n %{name}-%{version}
cp %{SOURCE1} ./Fedora-README.txt
iconv -f iso8859-1 -t utf-8 COPYING.txt > COPYING.txt.conv && mv -f COPYING.txt.conv COPYING.txt

%build
export CXXFLAGS="%{optflags} -std=c++0x"
# Passing a fake build name avoids default CMAKE_BUILD_TYPE="RelWithDebInfo"
# which has hard coded GCC optimizations.
%cmake \
    -DCMAKE_BUILD_TYPE=Fedora \
    -DCORE=ON -DBASE=ON -DD3XP=ON \
    -DDEDICATED=ON \
    -DSDL2=ON \
    neo
%cmake_build

%post
/usr/sbin/alternatives --install %{_bindir}/doom3-engine doom3-engine %{_bindir}/%{name} 10

%preun
if [ "$1" = 0 ]; then
    /usr/sbin/alternatives --remove doom3-engine %{_bindir}/%{name}
fi

%install
%cmake_install

%files
%license COPYING.txt
%doc README.md Fedora-README.txt
%{_bindir}/%{name}
%{_bindir}/%{name}ded
%{_libdir}/%{name}/

%changelog
* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Sun Apr 17 2022 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-9
- Update to 1.5.1 release

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-8.20201102gitbbe30e3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.1-7.20201102gitbbe30e3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.1-6.20201102gitbbe30e3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 04 2020 Simone Caronni <negativo17@gmail.com> - 1.5.1-5.20201102gitbbe30e3
- Update to latest snapshot.
- Drop CentOS/RHEL 7 support, ALSA is too old for updates.

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.1-4.20191103gitf24f18a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.1-3.20191103gitf24f18a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Nov 03 2019 Simone Caronni <negativo17@gmail.com> - 1.5.1-2.20191103gitf24f18a
- Update to snapshot post 1.5.1 Prerelease 1.

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.2-6.20170402gitd535e54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.2-5.20170402gitd535e54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.2-4.20170402gitd535e54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4.2-3.20170402gitd535e54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4.2-2.20170402gitd535e54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 06 2017 Simone Caronni <negativo17@gmail.com> - 1.4.2-1.20170402gitd535e54
- Update to latest snapshot (UHD resolution).
- Set snapshot release as per packaging guidelines.

* Sat Mar 25 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1rc1-3.89f227b
- Add ExcludeArch for ppc64le due to missing ppc_intrinsics.h

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4.1rc1-2.89f227b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 23 2016 Simone Caronni <negativo17@gmail.com> - 1.4.1rc1-1.89f227b
- Update to latest 1.4.1rc1.
- Drop RHEL 6 support, provided libjpeg is too old and would need to have a
  bundled jpeg_memory_src() function:
  https://github.com/dhewm/dhewm3/commit/657ad99bf185feb71199c6af097577d037e59d59
- Fix Fedora README file (it contained references to RBDoom3BFG...).
- Update License field as specified in the README.md file.
- Update Source URL as per packaging guidelines.
- Add license macro.

* Mon Mar 30 2015 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-23.git.657ad99
- Update to latest commits.

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.3.1.1304-22.git6d8108c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Dec 02 2013 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-21.git6d8108c
- Review fixes.

* Fri Nov 15 2013 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-20.git6d8108c5
- Updated.
- Added README.txt for game content.

* Thu Aug 22 2013 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-19.gitfa231898
- Updated.
- Remove unzip patch, upstreamed.
- Use SDL2 on Fedora 19+ and CentOS/RHEL 7+.

* Tue May 07 2013 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-18.git6407881c
- Updated.

* Sat Apr 13 2013 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-17.gitcedc129a
- Updated.

* Tue Jan 15 2013 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-16.git92a41322
- Updated.

* Fri Jan 04 2013 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-15.gitf8de7386
- Change fixedTic default.
- Added Z-fail compile time option.
- Update minizip code.

* Fri Dec 07 2012 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-13.git.f8de7386
- Updated.
- Removed display resolution autodetection, included upstream.
- Removed gl fix patch, included upstream.
- Updated no-cdkey patch.

* Tue Aug 28 2012 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-12.git.1b1787bb
- Auto detect resolution of monitor if single screen.
- Remove cd key check.
- Add EAX on by default.

* Thu Aug 09 2012 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-10.git.1b1787bb
- Updated, reverted "Don't use alpha bits for the GL config".
- Added dot in release tag for easier reading.
- Added alternatives system for doom3-engine.

* Mon Jul 23 2012 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-9.gitdf81835d
- Updated.

* Thu Jul 19 2012 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-8.git8aa0a4a9
- Updated, removed upstramed patch.

* Tue Jul 10 2012 Simone Caronni <negativo17@gmail.com> - 1.3.1.1304-7.gitf3ce725f
- First build.
