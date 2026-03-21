# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Sun Yuechi <sunyuechi@iscas.ac.cn>
# SPDX-FileContributor: yyjeqhc <jialin.oerv@isrc.iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%global _sbindir    /sbin
%global _libdir     /%{_lib}

%global _bashcompletiondir    /etc/bash_completion.d
%global _dracutdir  %{_prefix}/lib/dracut
%global _udevdir    %{_prefix}/lib/udev
%global _udevruledir    %{_prefix}/lib/udev/rules.d
%global _pkgconfigdir %{_prefix}/%{_lib}/pkgconfig

%define systemd_svcs zfs-import-cache.service zfs-import-scan.service zfs-mount.service zfs-mount@.service zfs-share.service zfs-zed.service zfs.target zfs-import.target zfs-volume-wait.service zfs-volumes.target

Name:           zfs-utils
Version:        2.4.1
Release:        %autorelease
Summary:        Commands to control the kernel modules and libraries
License:        CDDL
URL:            https://github.com/openzfs/zfs
#!RemoteAsset
Source0:        https://github.com/openzfs/zfs/releases/download/zfs-%{version}/zfs-%{version}.tar.gz
BuildSystem:    autotools

BuildOption(prep):  -n zfs-%{version}
BuildOption(conf):  --with-config=user
BuildOption(conf):  --with-udevdir=%{_udevdir}
BuildOption(conf):  --with-udevruledir=%{_udevruledir}
BuildOption(conf):  --with-dracutdir=%{_dracutdir}
BuildOption(conf):  --with-pamconfigsdir=%{_datadir}/pam-configs
BuildOption(conf):  --with-pammoduledir=%{_libdir}/security
BuildOption(conf):  --with-python=python3
BuildOption(conf):  --with-pkgconfigdir=%{_pkgconfigdir}
BuildOption(conf):  --disable-static
BuildOption(conf):  --disable-debug
BuildOption(conf):  --disable-debuginfo
BuildOption(conf):  --disable-asan
BuildOption(conf):  --disable-ubsan
BuildOption(conf):  --disable-pam
BuildOption(conf):  --enable-systemd
BuildOption(conf):  --with-systemdunitdir=%{_unitdir}
BuildOption(conf):  --with-systemdpresetdir=%{_presetdir}
BuildOption(conf):  --with-systemdmodulesloaddir=%{_modulesloaddir}
BuildOption(conf):  --with-systemdgeneratordir=%{_systemdgeneratordir}
BuildOption(conf):  --disable-sysvinit

BuildRequires:  make
BuildRequires:  python3
BuildRequires:  pkgconfig(zlib)
BuildRequires:  util-linux-devel
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libattr)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libtirpc)
BuildRequires:  systemd

Requires:       openssl
# The zpool iostat/status -c scripts call some utilities like lsblk and iostat
Requires:       util-linux
Requires:       sysstat
Requires:       zfs-libs%{?_isa} = %{version}-%{release}
Requires:       zfs-kmod = %{version}

%description
This package contains the core ZFS command line utilities.

%package     -n zfs-libs
Summary:        ZFS libraries for Linux

%description -n zfs-libs
This package contains the core ZFS libraries:
 * libzpool: Native ZFS pool library for managing zpools
 * libnvpair: Solaris name-value library for packing and unpacking data
 * libuutil: Solaris userland utility library providing compatibility functions
 * libzfs: Native ZFS filesystem library for managing ZFS filesystems

%package     -n zfs-devel
Summary:        Development headers
Requires:       zfs-libs%{?_isa} = %{version}-%{release}

%description -n zfs-devel
This package contains the header files needed for building additional
applications against the ZFS libraries.

%package        test
Summary:        Test infrastructure
BuildRequires:  libaio-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       parted
Requires:       lsscsi
Requires:       mdadm
Requires:       bc
Requires:       ksh
Requires:       fio
Requires:       acl
Requires:       sudo
Requires:       sysstat
Requires:       libaio
Requires:       python3
AutoReqProv:    no

%description    test
This package contains test infrastructure and support scripts for
validating the file system.

%package        dracut
Summary:        Dracut module
Requires:       %{name} >= %{version}
Requires:       dracut
Requires:       /usr/bin/awk
Requires:       grep

%description    dracut
This package contains a dracut module used to construct an initramfs
image which is ZFS aware.

%post
%systemd_post %{systemd_svcs}

%preun
%systemd_preun %{systemd_svcs}

%postun
%systemd_postun %{systemd_svcs}

%files
# Core utilities
%{_sbindir}/*
%{_bindir}/raidz_test
%{_bindir}/zvol_wait
# Optional Python 3 scripts
%{_bindir}/zarcsummary
%{_bindir}/zarcstat
%{_bindir}/dbufstat
%{_bindir}/zilstat
# Man pages
%{_mandir}/man1/*
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
# Configuration files and scripts
%{_libexecdir}/zfs
%{_udevdir}/vdev_id
%{_udevdir}/zvol_id
%{_udevdir}/rules.d/*
%{_datadir}/zfs/compatibility.d

# systemd files only
%exclude %{_sysconfdir}/zfs/zfs-functions
%exclude %{_sysconfdir}/default/zfs

%{_unitdir}/*
%{_presetdir}/*
%{_modulesloaddir}/*
%{_systemdgeneratordir}/*

%config(noreplace) %{_sysconfdir}/zfs/zed.d/*
%config(noreplace) %{_sysconfdir}/zfs/zpool.d/*
%config(noreplace) %{_sysconfdir}/zfs/vdev_id.conf.*.example
%attr(440, root, root) %config(noreplace) %{_sysconfdir}/sudoers.d/*

%config(noreplace) %{_bashcompletiondir}/zfs
%config(noreplace) %{_bashcompletiondir}/zpool

%files -n zfs-libs
%{_libdir}/libzpool.so.*
%{_libdir}/libnvpair.so.*
%{_libdir}/libuutil.so.*
%{_libdir}/libzfs*.so.*

%files -n zfs-devel
%{_pkgconfigdir}/libzfs.pc
%{_pkgconfigdir}/libzfsbootenv.pc
%{_pkgconfigdir}/libzfs_core.pc
%{_libdir}/*.so
%{_includedir}/*
%doc AUTHORS COPYRIGHT LICENSE NOTICE README.md

%files test
%{_datadir}/zfs/zfs-tests
%{_datadir}/zfs/test-runner
%{_datadir}/zfs/runfiles
%{_datadir}/zfs/*.sh

%files dracut
%doc contrib/dracut/README.md
%{_dracutdir}/modules.d/*

%exclude /usr/share/initramfs-tools

%changelog
%{?autochangelog}
