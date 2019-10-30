%define _disable_lto 1
%define debug_package %{nil}
%define dirver %(echo %{version}|sed -e 's/[a-z]//g')

%ifarch %{x86_64}
%global efiarch x86_64
%endif
%ifarch %{aarch64}
%global efiarch aarch64
%endif
%ifarch %{arm}
%global efiarch arm
%endif
%ifarch %{ix86}
%global efiarch ia32
%endif

Summary:	Development Libraries and headers for EFI
Name:		gnu-efi
Version:	3.0.11
Release:	1
Group:		System/Kernel and hardware
License:	BSD
Url:		http://sourceforge.net/projects/gnu-efi
Source0:	http://freefr.dl.sourceforge.net/project/gnu-efi/gnu-efi-%{version}.tar.bz2
Source100:	%{name}.rpmlintrc
Patch0:		gnu-efi-3.0.10-fallthroug.patch
Patch1:		https://sourceforge.net/p/gnu-efi/patches/70/attachment/gnu-efi-3.0.9-fix-clang-build.patch
BuildRequires:	glibc-devel
BuildRequires:	kernel-source

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%autosetup -n %{name}-%{dirver} -p1

%build
# (tpg) pass -z norelro for LLD
sed -i -e 's/build-id=sha1/build-id=sha1 -z norelro/g' Make.defaults
# or use LD.BFD
%ifarch %{ix86}
export LD=ld.bfd
%else
export LD=ld
%endif

# Make sure we don't need an executable stack
find . -name "*.S" |while read i; do
    if ! grep -q .note.GNU-stack $i; then
%ifarch armv7hnl
	echo '.section .note.GNU-stack,""' >>$i
%else
	echo '.section .note.GNU-stack,"",@progbits' >>$i
%endif
    fi
done

# Makefiles aren't SMP clean and do not pass our optflags and ldflags
make CC=%{__cc} HOSTCC=%{__cc} LD="$LD" PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot}
make apps CC=%{__cc} HOSTCC=%{__cc} LD="$LD" PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot}

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot}

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
