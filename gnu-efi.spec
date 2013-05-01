%define debug_package %{nil}
%define dirver	%(echo %{version}|sed -e 's/[a-z]//g')

Summary:	Development Libraries and headers for EFI
Name:		gnu-efi
Version:	3.0t
Release:	1
Group:		System/Kernel and hardware
License:	BSD
Url:		ftp://ftp.hpl.hp.com/pub/linux-ia64
Source0:	ftp://ftp.hpl.hp.com/pub/linux-ia64/%{name}_%{version}.orig.tar.gz
ExclusiveArch:	%{ix86} x86_64

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%setup -qn %{name}-%{dirver}
%apply_patches

%build
%make

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
%dir %{_libdir}/gnuefi
%{_libdir}/gnuefi/*
%{_libdir}/.a
%dir /boot/efi/EFI/rosa/
%attr(0644,root,root) /boot/efi/EFI/rosa/*.efi

