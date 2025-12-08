# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Yafen Fang <yafen@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           ltrace
Version:        0.8.1
Release:        %autorelease
Summary:        Tracks runtime library calls in dynamically linked programs
License:        GPL-2.0-or-later
URL:            https://ltrace.org/
#!RemoteAsset
Source0:        https://gitlab.com/cespedes/ltrace/-/archive/%{version}/ltrace-%{version}.tar.gz
BuildSystem:    autotools

BuildOption(conf):  --disable-werror

BuildRequires:  pkgconfig(libdw)
BuildRequires:  dejagnu
BuildRequires:  libselinux-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Ltrace is a debugging program which runs a specified command until the
command exits.  While the command is executing, ltrace intercepts and
records both the dynamic library calls called by the executed process
and the signals received by the executed process. Ltrace can also
intercept and print system calls executed by the process.

%conf -p
autoreconf -fiv

%files
%doc NEWS CREDITS INSTALL README TODO COPYING
%{_bindir}/ltrace
%{_datadir}/ltrace
%{_mandir}/man1/ltrace.1*
%{_mandir}/man5/ltrace.conf.5*

%changelog
%{?autochangelog}
