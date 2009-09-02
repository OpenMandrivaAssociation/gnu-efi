%define name	gnu-efi
%define version	3.0c
%define release	%mkrel 4

Summary:	Development Libraries and headers for EFI
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Development/Kernel
License:	GPL
URL:		ftp://ftp.hpl.hp.com/pub/linux-ia64/
Source0:	gnu-efi-%{version}.tar.bz2
Patch0:		gnu-efi-3.0c-makefile.patch
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	binutils
ExclusiveArch:	ia64 i586

%description
This package contains development headers and libraries for developing
EFI (Extensible Firmware Interface) applications.

%prep
%setup -q -n gnu-efi-%{version}
%patch0 -p1 -b .makefile

%build
# Doesn't like parallel make
make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}
make INSTALLROOT=$RPM_BUILD_ROOT%{_prefix} install

mkdir -p $RPM_BUILD_ROOT%{_libdir}/gnuefi
mv $RPM_BUILD_ROOT%{_libdir}/*.{o,lds} $RPM_BUILD_ROOT%{_libdir}/gnuefi

make -C apps clean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc README.* ChangeLog apps
%dir %{_includedir}/efi
%{_includedir}/efi/*.h
%ifarch i586
%{_includedir}/efi/ia32
%endif
%ifarch ia64
%{_includedir}/efi/ia64
%endif
%{_includedir}/efi/protocol
%dir %{_libdir}/gnuefi
%{_libdir}/*.a
%{_libdir}/gnuefi/*.o
%{_libdir}/gnuefi/*.lds

