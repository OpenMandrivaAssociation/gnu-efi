%define _disable_lto 1
%define debug_package %{nil}
%define dirver	%(echo %{version}|sed -e 's/[a-z]//g')

%ifarch x86_64
%global efiarch x86_64
%endif
%ifarch %{ix86}
%global efiarch ia32
%endif

Summary:	Development Libraries and headers for EFI
Name:		gnu-efi
Version:	3.0.6
Release:	1
Group:		System/Kernel and hardware
License:	BSD
Url:		http://sourceforge.net/projects/gnu-efi
Source0:	http://freefr.dl.sourceforge.net/project/gnu-efi/gnu-efi-%{version}.tar.bz2
Source100:	%{name}.rpmlintrc
# grub legacy makes use of setjmp/longjmp and assumes they're in libgnuefi.a
# so let's put them back there for now...
Patch0:		gnu-efi-3.0v-revert-setjmp-removal.patch
ExclusiveArch:	%{ix86} x86_64

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
%global optflags %{optflags} -Wno-error=-Wno-pointer-to-int-cast
%endif

%setup_compile_flags
# Makefiles aren't SMP clean
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
