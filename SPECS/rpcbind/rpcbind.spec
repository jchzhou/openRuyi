# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: yyjeqhc <1772413353@qq.com>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           rpcbind
Version:        1.2.8
Release:        %autorelease
Summary:        Transport independent RPC portmapper
License:        BSD-3-Clause
URL:            http://rpcbind.sourceforge.net
#!RemoteAsset
Source0:        https://downloads.sourceforge.net/sourceforge/rpcbind/rpcbind-%{version}.tar.bz2
Source1:        rpc-user.sysusers
BuildSystem:    autotools

BuildOption(conf): --disable-libwrap
BuildOption(conf): --enable-warmstarts
BuildOption(conf): --enable-debug
BuildOption(conf): --with-statedir=%{_rundir}/%{name}
BuildOption(conf): --with-rpcuser=rpc
BuildOption(conf): --with-systemdsystemunitdir=%{_unitdir}
BuildOption(conf): --with-nss-modules="files usrfiles"

BuildRequires:  libtirpc-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  autoconf automake
%{?systemd_ordering}

%description
Rpcbind is a replacement for portmap, providing a transport-independent
RPC portmapper for various protocols including IPv6.

%conf -p
autoreconf -fiv

%install -a
install -d %{buildroot}%{_sysusersdir}
install -m 644 %{SOURCE1} %{buildroot}%{_sysusersdir}/rpc-user.conf

%pre
%sysusers_create_package rpc-user %{SOURCE1}

%preun
%service_del_preun %{name}.service %{name}.socket

%post
%systemd_post %{name}.socket %{name}.service

%postun
%systemd_postun %{name}.socket %{name}.service

%files
%license COPYING
%doc AUTHORS README
%{_sbindir}/rpcbind
%{_bindir}/rpcinfo
%{_mandir}/*/*
%{_sysusersdir}/rpc-user.conf
%{_unitdir}/rpcbind.service
%{_unitdir}/rpcbind.socket

%changelog
%{?autochangelog}
