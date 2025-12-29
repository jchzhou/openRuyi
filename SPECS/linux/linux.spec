# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Jingwiw <wangjingwei@iscas.ac.cn>
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0
%global modpath %{_prefix}/lib/modules/%{kver}

%ifarch riscv64
#!BuildConstraint: hardware:jobs 32
%endif

# Whether dtbs needed for arch
%ifarch riscv64
%global need_dtbs 1
%else
%global need_dtbs 0
%endif

%global signmodules 1
%global kver %{version}-%{release}
%global kernel_make_flags LD=ld.bfd KBUILD_BUILD_VERSION=%{release}
Name:             linux
Version:          6.18.2
Release:          %autorelease
Summary:          The Linux Kernel
License:          GPL-2.0-only
URL:              https://www.kernel.org/

#!RemoteAsset:    sha256:558c6bbab749492b34f99827fe807b0039a744693c21d3a7e03b3a48edaab96a
Source0:          https://cdn.kernel.org/pub/linux/kernel/v6.x/%{name}-%{version}.tar.xz
Source1:          config.%{_arch}

Patch1001:        0001-UPSTREAM-drm-ttm-add-pgprot-handling-for-RISC-V.patch
Patch1002:        0002-UPSTREAM-riscv-sophgo-dts-add-PCIe-controllers-for-S.patch
Patch1003:        0003-UPSTREAM-riscv-sophgo-dts-enable-PCIe-for-PioneerBox.patch
Patch1004:        0004-UPSTREAM-riscv-sophgo-dts-enable-PCIe-for-SG2042_EVB.patch
Patch1005:        0005-UPSTREAM-riscv-sophgo-dts-enable-PCIe-for-SG2042_EVB.patch
Patch1006:        0006-UPSTREAM-riscv-dts-sophgo-Add-SPI-NOR-node-for-SG204.patch
Patch1007:        0007-UPSTREAM-riscv-dts-sophgo-Enable-SPI-NOR-node-for-Pi.patch
Patch1008:        0008-UPSTREAM-riscv-dts-sophgo-Enable-SPI-NOR-node-for-SG.patch
Patch1009:        0009-UPSTREAM-riscv-dts-sophgo-Enable-SPI-NOR-node-for-SG.patch
Patch1010:        0010-UPSTREAM-dt-bindings-net-sophgo-sg2044-dwmac-add-phy.patch
Patch1011:        0011-UPSTREAM-perf-vendor-events-riscv-add-T-HEAD-C920V2-.patch
Patch1012:        0012-UPSTREAM-rust-macros-Add-support-for-imports_ns-to-m.patch
Patch1013:        0013-UPSTREAM-pwm-Export-pwmchip_release-for-external-use.patch
Patch1014:        0014-UPSTREAM-rust-pwm-Add-Kconfig-and-basic-data-structu.patch
Patch1015:        0015-UPSTREAM-rust-pwm-Add-complete-abstraction-layer.patch
Patch1016:        0016-UPSTREAM-rust-pwm-Add-module_pwm_platform_driver-mac.patch
Patch1017:        0017-UPSTREAM-rust-pwm-Drop-wrapping-of-PWM-polarity-and-.patch
Patch1018:        0018-UPSTREAM-rust-pwm-Fix-broken-intra-doc-link.patch
Patch1019:        0019-UPSTREAM-pwm-Add-Rust-driver-for-T-HEAD-TH1520-SoC.patch
Patch1020:        0020-UPSTREAM-dt-bindings-pwm-thead-Add-T-HEAD-TH1520-PWM.patch
Patch1021:        0021-UPSTREAM-pwm-Fix-Rust-formatting.patch
Patch1022:        0022-UPSTREAM-pwm-th1520-Fix-clippy-warning-for-redundant.patch
Patch1023:        0023-UPSTREAM-pwm-th1520-Use-module_pwm_platform_driver-m.patch
Patch1024:        0024-UPSTREAM-lib-crypto-riscv-chacha-Avoid-s0-fp-registe.patch
Patch1025:        0025-UPSTREAM-pwm-th1520-Fix-missing-Kconfig-dependencies.patch
Patch1026:        0026-UPSTREAM-riscv-dts-thead-add-xtheadvector-to-the-th1.patch
Patch1027:        0027-UPSTREAM-riscv-dts-thead-add-ziccrse-for-th1520.patch
Patch1028:        0028-UPSTREAM-riscv-dts-thead-add-zfh-for-th1520.patch
Patch1029:        0029-UPSTREAM-riscv-dts-thead-Add-PWM-controller-node.patch
Patch1030:        0030-UPSTREAM-riscv-dts-thead-Add-PWM-fan-and-thermal-con.patch
Patch1031:        0031-UPSTREAM-dt-bindings-vendor-prefixes-Add-UltraRISC.patch
Patch1032:        0032-UPSTREAM-dt-bindings-interrupt-controller-Add-UltraR.patch
Patch1033:        0033-UPSTREAM-irqchip-sifive-plic-Cache-the-interrupt-ena.patch
Patch1034:        0034-UPSTREAM-irqchip-sifive-plic-Add-support-for-UltraRI.patch
Patch1035:        0035-UPSTREAM-lib-crypto-riscv-Add-poly1305-core.S-to-.gi.patch
Patch1036:        0036-FROMLIST-riscv-errata-Add-ERRATA_THEAD_WRITE_ONCE-fi.patch
Patch1037:        0037-FROMLIST-PCI-Release-BAR0-of-an-integrated-bridge-to.patch
Patch1038:        0038-BACKPORT-FROMLIST-drm-ttm-save-the-device-s-DMA-cohe.patch
Patch1039:        0039-BACKPORT-FROMLIST-drm-ttm-downgrade-cached-to-write_.patch
Patch1040:        0040-FROMLIST-dt-bindings-clock-thead-th1520-clk-ap-Add-I.patch
Patch1041:        0041-FROMLIST-clk-thead-th1520-ap-Poll-for-PLL-lock-and-w.patch
Patch1042:        0042-FROMLIST-clk-thead-th1520-ap-Add-C910-bus-clock.patch
Patch1043:        0043-FROMLIST-clk-thead-th1520-ap-Support-setting-PLL-rat.patch
Patch1044:        0044-FROMLIST-clk-thead-th1520-ap-Add-macro-to-define-mul.patch
Patch1045:        0045-FROMLIST-clk-thead-th1520-ap-Support-CPU-frequency-s.patch
Patch1046:        0046-FROMLIST-NFU-riscv-dts-thead-Add-CPU-clock-and-OPP-t.patch
Patch1047:        0047-FROMLIST-dt-bindings-vendor-prefixes-add-verisilicon.patch
Patch1048:        0048-FROMLIST-dt-bindings-display-add-verisilicon-dc.patch
Patch1049:        0049-FROMLIST-drm-verisilicon-add-a-driver-for-Verisilico.patch
Patch1050:        0050-FROMLIST-dt-bindings-display-bridge-add-binding-for-.patch
Patch1051:        0051-FROMLIST-drm-bridge-add-a-driver-for-T-Head-TH1520-H.patch
Patch1052:        0052-FROMLIST-riscv-dts-thead-add-DPU-and-HDMI-device-tre.patch
Patch1053:        0053-FROMLIST-riscv-dts-thead-lichee-pi-4a-enable-HDMI.patch
Patch1054:        0054-FROMLIST-MAINTAINERS-assign-myself-as-maintainer-for.patch
Patch1055:        0055-FROMLIST-mailmap-map-all-Icenowy-Zheng-s-mail-addres.patch
Patch1056:        0056-FROMLIST-dt-bindings-usb-Add-T-HEAD-TH1520-USB-contr.patch
Patch1057:        0057-FROMLIST-usb-dwc3-add-T-HEAD-TH1520-usb-driver.patch
Patch1058:        0058-FROMLIST-rust-export-BINDGEN_TARGET-from-a-separate-.patch
Patch1059:        0059-FROMLIST-rust-generate-a-fatal-error-if-BINDGEN_TARG.patch
Patch1060:        0060-FROMLIST-rust-add-a-Kconfig-function-to-test-for-sup.patch
Patch1061:        0061-FROMLIST-RISC-V-handle-extension-configs-for-bindgen.patch
Patch1062:        0062-FROMLIST-PCI-MSI-Conservatively-generalize-no_64bit_.patch
Patch1063:        0063-FROMLIST-PCI-MSI-Check-msi_addr_mask-in-msi_verify_e.patch
Patch1064:        0064-FROMLIST-drm-radeon-Raise-msi_addr_mask-to-40-bits-f.patch
Patch1065:        0065-FROMLIST-ALSA-hda-intel-Raise-msi_addr_mask-to-dma_b.patch
Patch1066:        0066-FROMLIST-PCI-ASPM-Avoid-L0s-and-L1-on-Sophgo-2042-PC.patch
Patch1067:        0067-FROMLIST-PCI-ASPM-Avoid-L0s-and-L1-on-Sophgo-2044-PC.patch
Patch1068:        0068-XUANTIE-riscv-dts-th1520-add-licheepi4a-16g-support.patch
Patch1069:        0069-XUANTIE-riscv-dts-thead-Add-TH1520-USB-nodes.patch
Patch1070:        0070-XUANTIE-riscv-dts-thead-Add-TH1520-I2C-nodes.patch
Patch1071:        0071-XUANTIE-riscv-dts-thead-Add-Lichee-Pi-4A-IO-expansio.patch
Patch1072:        0072-XUANTIE-riscv-dts-thead-Enable-Lichee-Pi-4A-USB.patch
Patch1073:        0073-REVYOS-riscv-dts-th1520-rename-thead-to-xuantie.patch
Patch1074:        0074-REVYOS-riscv-dts-th1520-add-xuantie-th1520-mbox-r.patch
Patch1075:        0075-SOPHGO-dt-bindings-nvmem-Add-SG2044-eFuse-controller.patch
Patch1076:        0076-SOPHGO-nvmem-Add-Sophgo-SG2044-eFuse-driver.patch
Patch1077:        0077-SOPHGO-riscv-dts-sophgo-sg2044-Add-eFUSE-device.patch
Patch1078:        0078-SOPHGO-dts-sg2044-Modify-pcie-bar-address.patch
Patch1079:        0079-REVYSR-dt-bindings-net-ultrarisc-dp1000-gmac-Add-sup.patch
Patch1080:        0080-REVYSR-net-stmmac-add-support-for-dwmac-5.10a.patch
Patch1081:        0081-RVCK-riscv-dp1000-8250_dw-support-ultrarisc-dp1000-u.patch
Patch1082:        0082-RVCK-riscv-dts-add-dp1000.dts-for-UltraRIsc-DP1000-S.patch
Patch1083:        0083-RVCK-riscv-dp1000-arch-add-UltraRISC-DP1000-SoC-supp.patch
Patch1084:        0084-RVCK-riscv-dp1000-pci-support-UltraRISC-pcie-rc.patch
Patch1085:        0085-RVCK-pcie-update-the-outbound-mapping-process.patch
Patch1086:        0086-RVCK-pinctrl-add-pinctrl-dirver-for-UltraRisc-DP1000.patch
Patch1087:        0087-RVCK-dts-add-pinctrl-dtsi-dts-for-UltraRisc-DP1000.patch
Patch1088:        0088-RVCK-pci-Update-the-number-of-outbound-and-inbound.patch
Patch1089:        0089-RVCK-riscv-dp1000-pci-Add-custom-PCI-host-ops.patch
Patch1090:        0090-RVCK-riscv-dp1000-dts-add-the-dts-of-UltraRISC-dp100.patch
Patch1091:        0091-RVCK-riscv-dp1000-dts-Move-mmc0-node-from-SoC-to-boa.patch
Patch1092:        0092-RVCK-riscv-dp1000-plic-add-plic-early-init-supports.patch
Patch1093:        0093-RVCK-pcie-ultrarisc-Add-suspend-resume-support.patch
Patch1094:        0094-RVCK-riscv-dp1000-dts-Move-chosen-node-from-common-t.patch
Patch1095:        0095-RVCK-dts-riscv-ultrarisc-Refactor-DP1000-device-tree.patch
Patch1096:        0096-RVCK-riscv-pinctrl-ultrarisc-Implement-pin-configura.patch
Patch1097:        0097-RVCK-riscv-dts-dp1000-add-dts-dtsi-for-Milk-V-Titan-.patch

BuildRequires:    gcc, bison, binutils, glibc-devel, make, perl
BuildRequires:    flex, bison
BuildRequires:    bc, cpio, dwarves, gettext, python3, rsync, tar, xz, zstd
BuildRequires:    libasm-devel
BuildRequires:    libdebuginfod-dummy-devel
BuildRequires:    ncurses-devel
BuildRequires:    libcap-devel
BuildRequires:    libssh-devel
BuildRequires:    libdw-devel
BuildRequires:    libelf-devel
BuildRequires:    zstd-devel
BuildRequires:    python3-devel
BuildRequires:    slang-devel
BuildRequires:    zlib-devel
BuildRequires:    openssl-devel
BuildRequires:    kmod
BuildRequires:    rpm-config-openruyi

Requires:       %{name}-core%{?_isa} = %{version}-%{release}
Requires:       %{name}-modules%{?_isa} = %{version}-%{release}
%if %{need_dtbs}
Requires:       %{name}-dtbs%{?_isa} = %{version}-%{release}
%endif
Requires(post):   kmod
Requires(post):   kernel-install
Requires(postun): kernel-install
%description
This is a meta-package that installs the core kernel image and modules.
For a minimal boot environment, install the 'linux-core' package instead.

%package core
Summary:        The core Linux kernel image and initrd

%description core
Contains the bootable kernel image (vmlinuz) and a generic, pre-built initrd,
providing the minimal set of files needed to boot the system.

%package modules
Summary:        Kernel modules for the Linux kernel
Requires:       %{name}-core = %{version}-%{release}

%description modules
Contains all the kernel modules (.ko files) and associated metadata for
the hardware drivers and kernel features.

%package devel
Summary:          Development files for building external kernel modules
Requires:         %{name} = %{version}-%{release}
Requires:         dwarves

%description devel
This package provides the kernel headers and Makefiles necessary to build
external kernel modules against the installed kernel. The development files are
located at %{_usrsrc}/kernels/%{kver}, with symlinks provided under
%{_prefix}/lib/modules/%{kver}/ for compatibility.

%if %{need_dtbs}

%package dtbs
Summary:          Devicetree blob files from Linux sources

%description dtbs
This package provides the DTB files built from Linux sources that may be used
for booting.

%endif

%prep
%autosetup -p1
cp %{SOURCE1} .config
echo "-%{release}" > localversion

%conf
%make_build %{kernel_make_flags} olddefconfig

%build

%make_build %{kernel_make_flags}

%if %{need_dtbs}
%make_build %{kernel_make_flags} dtbs
%endif

%install
%define ksrcpath %{buildroot}%{_usrsrc}/kernels/%{kver}
install -d %{buildroot}%{modpath} %{ksrcpath}

%make_build %{kernel_make_flags} INSTALL_MOD_PATH=%{buildroot}%{_prefix} INSTALL_MOD_STRIP=1 DEPMOD=true modules_install

%if %{need_dtbs}
%make_build %{kernel_make_flags} INSTALL_DTBS_PATH=%{buildroot}%{modpath}/dtb dtbs_install
%endif

%make_build run-command %{kernel_make_flags} KBUILD_RUN_COMMAND="$(pwd)/scripts/package/install-extmod-build %{ksrcpath}"

pushd %{buildroot}%{modpath}
ln -sf %{_usrsrc}/kernels/%{kver} build
ln -sf %{_usrsrc}/kernels/%{kver} source
popd

install -Dm644 $(make %{kernel_make_flags} -s image_name) %{buildroot}%{modpath}/vmlinuz

echo "Module signing would happen here for version %{kver}."

%post
%{_bindir}/kernel-install add %{kver} %{modpath}/vmlinuz

%postun
if [ $1 -eq 0 ] ; then
    %{_bindir}/kernel-install remove %{kver}
fi

%files
%license COPYING
%doc README

%files core
%{modpath}/vmlinuz

%files modules
%{modpath}/*
%exclude %{modpath}/vmlinuz
%exclude %{modpath}/build
%exclude %{modpath}/source

%files devel
%{_usrsrc}/kernels/%{kver}/
%{modpath}/build
%{modpath}/source

%if %{need_dtbs}
%files dtbs
%{modpath}/dtb
%endif

%changelog
%{?autochangelog}
