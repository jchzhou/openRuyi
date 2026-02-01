# SPDX-FileCopyrightText: (C) 2025, 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025, 2026 openRuyi Project Contributors
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           appstream
Version:        1.1.1
Release:        %autorelease
Summary:        Utilities to generate, maintain and access the AppStream database
License:        LGPL-2.1-or-later
URL:            https://github.com/ximion/appstream
#!RemoteAsset:  sha256:
#!RemoteAsset
Source:         https://github.com/ximion/appstream/archive/refs/tags/v%{version}.tar.gz
BuildSystem:    meson

BuildOption(conf):  -Ddocs=false
BuildOption(conf):  -Dapidocs=false
BuildOption(conf):  -Dman=false
BuildOption(conf):  -Dinstall-docs=false
BuildOption(conf):  -Dqt=true
BuildOption(conf):  -Dcompose=false
BuildOption(conf):  -Dstemming=false

BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libfyaml)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(xmlb)
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  itstool
BuildRequires:  gperf

%description
AppStream is a cross-distro effort for providing metadata for software
components in the Linux ecosystem.

%package        devel
Summary:        Development files for libappstream
Requires:       appstream%{?_isa} = %{version}-%{release}

%description    devel
Development files for AppStream.

%package        qt-devel
Summary:        Development files for %{name}-qt bindings
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig(Qt6Core) >= 6.2.4

%description    qt-devel
%{summary}.

%install -a
# Avoid illegal package names
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/*@*
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/en_GB/
%find_lang %{name} --generate-subpackages

%files
%{_bindir}/appstreamcli
%{_datadir}/appstream/appstream.conf
%{_datadir}/gettext/its/metainfo.*
%{_datadir}/metainfo/org.freedesktop.appstream.cli.metainfo.xml
%exclude %{_datadir}/installed-tests/
%{_libdir}/libappstream.so.*
%{_libdir}/girepository-1.0/*.typelib
%{_libdir}/libAppStreamQt.so.*

%files    devel
%{_includedir}/appstream/
%{_libdir}/libappstream.so
%{_libdir}/pkgconfig/appstream.pc
%{_datadir}/gir-1.0/*.gir

%files qt-devel
%{_includedir}/AppStreamQt/
%{_libdir}/cmake/AppStreamQt/
%{_libdir}/libAppStreamQt.so

%changelog
%{?autochangelog}
