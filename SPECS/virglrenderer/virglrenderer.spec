# SPDX-FileCopyrightText: (C) 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2026 openRuyi Project Contributors
# SPDX-FileContributor: jchzhou <zhoujiacheng@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

# test with llvmpipe
%bcond tests 1

Name:           virglrenderer
Version:        1.3.0
Release:        %autorelease
Summary:        VirGL virtual OpenGL renderer
License:        MIT
URL:            https://virgil3d.github.io/
VCS:            git:https://gitlab.freedesktop.org/virgl/virglrenderer.git
#!RemoteAsset:  sha256:065bc56e89e6f631f96101cd62eba0748e48eb888b434edc86e89d05395e76f3
Source0:        https://gitlab.freedesktop.org/virgl/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
BuildSystem:    meson

BuildOption(conf):  -Ddrm-renderers=amdgpu-experimental,panfrost-experimental,asahi,msm,i915-experimental
BuildOption(conf):  -Dvenus=true
BuildOption(conf):  -Dvideo=true
%if %{with tests}
BuildOption(conf):  -Dtests=true
%else
BuildOption(conf):  -Dtests=false
%endif

BuildRequires:  meson
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libdrm_amdgpu)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(x11)
BuildRequires:  python3dist(pyyaml)
%if %{with tests}
BuildRequires:  pkgconfig(check)
BuildRequires:  mesa-dril
BuildRequires:  mesa-gl
%endif

# venus (vulkan) dlopen's libvulkan
Requires:       vulkan-loader

%description
virglrenderer is a virtual 3D GPU library that allows a guest operating
system, such as a virtual machine managed by QEMU, to use the host GPU to
accelerate 3D rendering through the virtio GPU (virgl) interface.

It provides an OpenGL renderer (vrend), a Vulkan renderer (venus) that
forwards guest Vulkan commands to the host Vulkan driver, native DRM
contexts for AMD, Intel, Panfrost, Asahi and MSM GPUs, and optional hardware
video acceleration.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains the libraries, headers and pkg-config
files needed to develop applications that use %{name}. It is required to
build QEMU with virgl 3D acceleration support.

%package        test-server
Summary:        Testing server for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    test-server
The %{name}-test-server package contains virgl_test_server, a server that
can be used together with the Mesa virgl driver to test virgl rendering
without a compositor or a display server.

%check
%if %{with tests}
# Diagnostic probe: resolve the exact EGL entry points virgl_egl_get_funcs()
# needs, both through libEGL and through libepoxy, and then run the surfaceless
# sequence via epoxy. Non-fatal; remove once the tests pass.
python3 - <<'PYEOF' || :
import ctypes

epoxy = ctypes.CDLL("libepoxy.so.0")
le = ctypes.CDLL("libEGL.so.1")


def epoxy_fn(sym, restype, argtypes):
    p = ctypes.c_void_p.in_dll(epoxy, sym)
    return ctypes.CFUNCTYPE(restype, *argtypes)(p.value)


qstring = epoxy_fn("epoxy_eglQueryString", ctypes.c_char_p, [ctypes.c_void_p, ctypes.c_int])
gpa = epoxy_fn("epoxy_eglGetProcAddress", ctypes.c_void_p, [ctypes.c_char_p])
geterr = epoxy_fn("epoxy_eglGetError", ctypes.c_int, [])
initialize = epoxy_fn("epoxy_eglInitialize", ctypes.c_uint, [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)])

le.eglGetProcAddress.restype = ctypes.c_void_p
le.eglGetProcAddress.argtypes = [ctypes.c_char_p]

cext = qstring(None, 0x3055) or b""
for flag in (b"EGL_EXT_platform_base", b"EGL_EXT_device_query", b"EGL_EXT_device_enumeration"):
    print(f"client has {flag.decode()}: {flag in cext}")

names = (b"eglGetPlatformDisplayEXT", b"eglQueryDeviceAttribEXT", b"eglQueryDeviceStringEXT",
         b"eglQueryDisplayAttribEXT", b"eglQueryDevicesEXT")
for n in names:
    print(f"{n.decode()}: libEGL={hex(le.eglGetProcAddress(n) or 0)} epoxy={hex(gpa(n) or 0)}")

addr = gpa(b"eglGetPlatformDisplayEXT")
if not addr:
    raise SystemExit(0)
gpd = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p)(addr)
dpy = gpd(0x31DD, None, None)  # EGL_PLATFORM_SURFACELESS_MESA, EGL_DEFAULT_DISPLAY
print(f"surfaceless display: {hex(dpy) if dpy else None} err=0x{geterr():x}")
if not dpy:
    raise SystemExit(0)
ma, mi = ctypes.c_int(), ctypes.c_int()
ok = initialize(dpy, ctypes.byref(ma), ctypes.byref(mi))
print(f"eglInitialize: {ok} EGL {ma.value}.{mi.value} err=0x{geterr():x}")
if not ok:
    raise SystemExit(0)
dext = qstring(dpy, 0x3055) or b""
print(f"display has EGL_KHR_surfaceless_context: {b'EGL_KHR_surfaceless_context' in dext}")
print(f"display has EGL_KHR_create_context: {b'EGL_KHR_create_context' in dext}")
PYEOF

# for headless environment
GALLIUM_DRIVER=llvmpipe \
LIBGL_ALWAYS_SOFTWARE=1 \
LIBGL_DEBUG=verbose \
EGL_LOG_LEVEL=debug \
VRENDTEST_USE_EGL_SURFACELESS=1 %meson_test
%endif

%files
%license COPYING
%{_libdir}/libvirglrenderer.so.1*
# helper process used by the venus Vulkan renderer
%{_libexecdir}/virgl_render_server

%files devel
%dir %{_includedir}/virgl/
%{_includedir}/virgl/*.h
%{_libdir}/libvirglrenderer.so
%{_libdir}/pkgconfig/virglrenderer.pc

%files test-server
%{_bindir}/virgl_test_server

%changelog
%autochangelog
