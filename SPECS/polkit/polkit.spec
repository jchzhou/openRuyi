# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: yyjeqhc <1772413353@qq.com>
#
# SPDX-License-Identifier: MulanPSL-2.0

Name:           polkit
Version:        126
Release:        %autorelease
Summary:        PolicyKit Authorization Framework
License:        LGPL-2.1-or-later
URL:            https://gitlab.freedesktop.org/polkit/polkit/
#!RemoteAsset
Source0:        https://github.com/polkit-org/polkit/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        50-default.rules
BuildSystem:    meson

BuildOption(conf):    -D session_tracking=logind
BuildOption(conf):    -D systemdsystemunitdir="%{_unitdir}"
BuildOption(conf):    -D os_type=suse
BuildOption(conf):    -D pam_module_dir="%{_pam_moduledir}"
BuildOption(conf):    -D pam_prefix="%{_pam_vendordir}"
BuildOption(conf):    -D examples=false
BuildOption(conf):    -D tests=false
BuildOption(conf):    -D man=false
BuildOption(conf):    -D c_args="%{optflags} -Wno-error=deprecated-declarations"
BuildOption(conf):    -D introspection=false
BuildOption(conf):    -D gtk_doc=false

BuildRequires:  python3 meson ninja
BuildRequires:  gcc-c++ expat-devel pam-devel pkgconfig
BuildRequires:  pkgconfig(duktape) >= 2.2.0
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(libsystemd)

%systemd_ordering

%description
PolicyKit is a toolkit for defining and handling authorizations.

%package devel
Summary:        Development files for PolicyKit
Requires:       %{name} = %{version}
Requires:       pkgconfig

%description devel
Development files for the PolicyKit Authorization Framework.

%install -a
install -d %{buildroot}%{_localstatedir}/lib/polkit
install -m0644 %{SOURCE1} %{buildroot}%{_datadir}/polkit-1/rules.d/
mkdir -p %{buildroot}%{_sysconfdir}/polkit-1/actions
rm -rf %{buildroot}%{_datadir}/locale

%post
# The implied (systemctl preset) will fail and complain, but the macro hides
# and ignores the fact.  This is in fact what we want, polkit.service does not
# have an [Install] section and it is always started on demand.
%systemd_post polkit.service

%preun
%systemd_preun polkit.service

%postun
%systemd_postun_with_restart polkit.service

%files
%license COPYING
%doc NEWS.md README.md
%{_libdir}/libpolkit-agent-1.so.*
%{_libdir}/libpolkit-gobject-1.so.*
%{_bindir}/pkaction
%{_bindir}/pkcheck
%{_bindir}/pkttyagent
%verify(not mode) %attr(4755,root,root) %{_bindir}/pkexec
%dir /usr/lib/polkit-1
/usr/lib/polkit-1/polkitd
%verify(not mode) %attr(4755,root,root) /usr/lib/polkit-1/polkit-agent-helper-1
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/system-services
%{_datadir}/dbus-1/system-services/org.freedesktop.PolicyKit1.service
%dir %{_datadir}/dbus-1/system.d
%{_datadir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%dir %{_datadir}/polkit-1
%{_datadir}/polkit-1/policyconfig-1.dtd
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%attr(0555,root,root) %dir %{_datadir}/polkit-1/rules.d
%{_datadir}/polkit-1/rules.d/50-default.rules
%{_pam_vendordir}/polkit-1
%dir %{_sysconfdir}/polkit-1
%attr(0750,root,polkitd) %dir %{_sysconfdir}/polkit-1/rules.d
%dir %{_sysconfdir}/polkit-1/actions
%dir %{_localstatedir}/lib/polkit
%{_unitdir}/polkit.service
%{_sysusersdir}/polkit.conf
%{_tmpfilesdir}/polkit-tmpfiles.conf
%{_datadir}/gettext/its/polkit.its
%{_datadir}/gettext/its/polkit.loc

%files devel
%{_libdir}/libpolkit-agent-1.so
%{_libdir}/libpolkit-gobject-1.so
%{_libdir}/pkgconfig/polkit-agent-1.pc
%{_libdir}/pkgconfig/polkit-gobject-1.pc
%{_includedir}/polkit-1/

%changelog
%{?autochangelog}
