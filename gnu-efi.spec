%define _disable_lto 1
%define debug_package %{nil}
%define dirver	%(echo %{version}|sed -e 's/[a-z]//g')

%ifarch x86_64 znver1
%global efiarch x86_64
%endif
%ifarch aarch64
%global efiarch aarch64
%endif
%ifarch %{arm} armv7hnl
%global efiarch arm
%endif
%ifarch %{ix86}
%global efiarch ia32
%endif

Summary:	Development Libraries and headers for EFI
Name:		gnu-efi
Version:	3.0.8
Release:	1
Group:		System/Kernel and hardware
License:	BSD
Url:		http://sourceforge.net/projects/gnu-efi
Source0:	http://freefr.dl.sourceforge.net/project/gnu-efi/gnu-efi-%{version}.tar.bz2
Source100:	%{name}.rpmlintrc
# grub legacy makes use of setjmp/longjmp and assumes they're in libgnuefi.a
# so let's put them back there for now...
Patch0:		gnu-efi-3.0v-revert-setjmp-removal.patch
# (tpg) patches from fedora
Patch0001:	0001-PATCH-Disable-AVX-instruction-set-on-IA32-and-x86_64.patch
Patch0002:	0002-Use-ARFLAGS-when-invoking-ar.patch
Patch0003:	0003-Stripped-diff-for-makefile.patch
Patch0004:	0004-Make-sure-stdint.h-is-always-used-with-MSVC-on-ARM-A.patch
Patch0005:	0005-Add-EFI_DRIVER_ENTRY_POINT-support-for-MSVC-ARM64.patch
Patch0006:	0006-Move-memcpy-memset-definition-to-global-init.c.patch
Patch0007:	0007-Bump-revision-from-VERSION-3.0.6-to-VERSION-3.0.7.patch
Patch0008:	0008-Currently-we-have-DivU64x32-on-ia32-but-it-tries-to-.patch
Patch0009:	0009-gnuefi-preserve-.gnu.hash-sections-unbreaks-elilo-on.patch
Patch0010:	0010-gnu-efi-fix-lib-ia64-setjmp.S-IA-64-build-failure.patch
Patch0011:	0011-Fix-some-types-gcc-doesn-t-like.patch
Patch0012:	0012-Fix-arm-build-paths-in-the-makefile.patch
Patch0013:	0013-Work-around-Werror-maybe-uninitialized-not-being-ver.patch
Patch0014:	0014-Fix-a-sign-error-in-the-debughook-example-app.patch
Patch0015:	0015-Fix-typedef-of-EFI_PXE_BASE_CODE.patch
Patch0016:	0016-make-clang-not-complain-about-fno-merge-all-constant.patch
Patch0017:	0017-Fix-another-place-clang-complains-about.patch
Patch0018:	0018-gnu-efi-add-some-more-common-string-functions.patch
Patch0019:	0019-Add-D-to-print-device-paths.patch
Patch0020:	0020-Make-ARCH-overrideable-on-the-command-line.patch
Patch0021:	0021-apps-Add-bltgrid-and-lfbgrid-and-add-error-checks-to.patch
Patch0022:	0022-Nerf-Werror-pragma-away.patch
Patch0023:	0023-Call-ar-in-deterministic-mode.patch
Patch0024:	0024-Add-debug-helper-applications.patch
Patch0025:	0025-Bump-revision-from-VERSION-3.0.7-to-VERSION-3.0.8.patch
Patch0026:	0026-Use-EFI-canonical-names-everywhere-the-compiler-does.patch

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%setup -qn %{name}-%{dirver}
%apply_patches
sed -i -e 's,-fpic,-fpic -fuse-ld=bfd,g' Make.defaults

%build
%ifarch %{ix86}
# (tpg) fix build on i586
export CC=gcc
export CXX=g++
%endif

# Makefiles aren't SMP clean and do not pass our optflags
make PREFIX=%{_prefix} LIBDIR=%{_libdir} LD=ld.bfd INSTALLROOT=%{buildroot}
make apps PREFIX=%{_prefix} LIBDIR=%{_libdir} LD=ld.bfd INSTALLROOT=%{buildroot}

%install
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} install

mkdir -p %{buildroot}%{_libdir}/gnuefi
mv %{buildroot}/%{_libdir}/*.lds %{buildroot}/%{_libdir}/*.o %{buildroot}/%{_libdir}/gnuefi

mkdir -p %{buildroot}/boot/efi/EFI/openmandriva
cp -a %{efiarch}/apps/*.efi %{buildroot}/boot/efi/EFI/openmandriva/

%files
%doc README.* ChangeLog
%{_includedir}/efi
%{_libdir}/gnuefi
%{_libdir}/*.a
%dir /boot/efi/EFI/openmandriva/
%attr(0644,root,root) /boot/efi/EFI/openmandriva/*.efi
