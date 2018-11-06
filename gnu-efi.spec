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
Version:	3.0.9
Release:	1
Group:		System/Kernel and hardware
License:	BSD
Url:		http://sourceforge.net/projects/gnu-efi
Source0:	http://freefr.dl.sourceforge.net/project/gnu-efi/gnu-efi-%{version}.tar.bz2
Source100:	%{name}.rpmlintrc
# (tpg) patches from fedora
Patch0001: 0001-PATCH-Disable-AVX-instruction-set-on-IA32-and-x86_64.patch
BuildRequires:	glibc-devel
BuildRequires:	gcc
BuildRequires:	gcc-c++

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%autosetup -n %{name}-%{dirver} -p1

#sed -i -e 's,-fpic,-fpic -fuse-ld=bfd,g' Make.defaults

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

%build
# (tpg) build only with gcc
export CC=gcc
export CXX=g++

# Makefiles aren't SMP clean and do not pass our optflags
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot}
make apps PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot}

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
