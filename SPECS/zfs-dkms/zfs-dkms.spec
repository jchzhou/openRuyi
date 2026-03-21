# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Sun Yuechi <sunyuechi@iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

# Exclude input files from mangling
%global __brp_mangle_shebangs_exclude_from ^/%{_usrsrc}/.*$

%define module  zfs
%define mkconf  scripts/dkms.mkconf

Name:           %{module}-dkms
Version:        2.4.1
Release:        %autorelease
Summary:        Kernel module(s) (dkms)
License:        CDDL
URL:            https://github.com/openzfs/zfs
#!RemoteAsset
Source0:        https://github.com/openzfs/zfs/releases/download/zfs-%{version}/zfs-%{version}.tar.gz
BuildArch:      noarch

Requires:       dkms >= 2.2.0.3
Requires:       gcc
Requires:       make
Requires:       perl
Requires:       diffutils
Requires:       linux-devel

Provides:       %{module}-kmod = %{version}

AutoReqProv:    no

%description
This package contains the dkms ZFS kernel modules.

%prep
%autosetup -n zfs-%{version}

%build
%{mkconf} -n %{module} -v %{version} -f dkms.conf

%install
mkdir -p $RPM_BUILD_ROOT/%{_usrsrc}
cp -rf ${RPM_BUILD_DIR}/%{module}-%{version} $RPM_BUILD_ROOT/%{_usrsrc}/%{module}-%{version}

%files
%{_usrsrc}/%{module}-%{version}

%pre
echo "Running pre installation script: $0. Parameters: $*"

# Remove any existing ZFS DKMS modules to ensure clean installation
dkms_root=/var/lib/dkms
if [ -d ${dkms_root}/%{module} ]; then
    cd ${dkms_root}/%{module}
    for x in [[:digit:]]*; do
        [ -d "$x" ] || continue
        otherver="$x"
        if [ `dkms status -m %{module} -v "$otherver" | grep -c %{module}` -gt 0 ]; then
            echo "Removing old %{module} dkms modules version $otherver from all kernels."
            dkms remove -m %{module} -v "$otherver" --all ||:
        fi
    done
    cd ${dkms_root}
fi

%post
echo "Running post installation script: $0. Parameters: $*"

# Add the module to dkms
echo "Adding %{module} dkms modules version %{version} to dkms."
dkms add -m %{module} -v %{version} --rpm_safe_upgrade ||:

# Install the module for the current kernel with force overwrite
echo "Installing %{module} dkms modules version %{version} for the current kernel."
dkms install --force -m %{module} -v %{version} ||:

%preun
echo "Running pre uninstall script: $0. Parameters: $*"

# Skip removal on upgrade (RPM upgrade parameter is "1")
if [ "$1" = "1" ]; then
    echo "This is an upgrade. Skipping pre uninstall action."
    exit 0
fi

# Remove on uninstall (RPM uninstall parameter is "0")
if [ "$1" = "0" ]; then
    if [ `dkms status -m %{module} -v %{version} | grep -c %{module}` -gt 0 ]; then
        echo "Removing %{module} dkms modules version %{version} from all kernels."
        dkms remove -m %{module} -v %{version} --all --rpm_safe_upgrade
    fi
fi

exit 0

%changelog
%{?autochangelog}
