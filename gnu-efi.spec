Summary:	Development Libraries and headers for EFI
Name:		gnu-efi
Version:	3.0q
Release:	2
Group:		Development/System
License:	BSD
URL:		ftp://ftp.hpl.hp.com/pub/linux-ia64
Source0:	ftp://ftp.hpl.hp.com/pub/linux-ia64/gnu-efi-%{version}.tar.gz
Patch0:		gnu-efi-3.0q-Fix-usage-of-INSTALLROOT-PREFIX-and-LIBDIR.patch
Patch1:		gnu-efi-3.0q-route80h.patch
Patch2:		gnu-efi-3.0q-modelist.patch
Patch3:		gnu-efi-3.0q-route80h-add-cougarpoint.patch
Patch4:		gnu-efi-3.0q-machine-types.patch
Patch5:		gnu-efi-3.0q-handle-uninitialized-gop.patch
Patch6:		gnu-efi-3.0q-Add-.S-and-.E-rules.patch
ExclusiveArch:	%{ix86} x86_64

%define debug_package %{nil}

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%setup -q
%apply_patches

%build
# Package cannot build with %{?_smp_mflags}.
make

%install
mkdir -p %{buildroot}%{_libdir}

make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} install

mkdir -p %{buildroot}%{_libdir}/gnuefi
mv %{buildroot}%{_libdir}/*.lds %{buildroot}%{_libdir}/*.o %{buildroot}%{_libdir}/gnuefi

make -C apps clean route80h.efi modelist.efi
mkdir -p %{buildroot}/boot/efi/EFI/rosa/
mv apps/{route80h.efi,modelist.efi} %{buildroot}/boot/efi/EFI/rosa/

%files
%doc README.* ChangeLog
%{_includedir}/efi
%{_libdir}/*
%dir /boot/efi/EFI/rosa/
%attr(0644,root,root) /boot/efi/EFI/rosa/*.efi

%changelog
* Fri Jul 27 2012 Matthew Garrett <mjg@redhat.com> - 3.0q-1
- Update to current upstream
- License change - GPLv2+ to BSD

