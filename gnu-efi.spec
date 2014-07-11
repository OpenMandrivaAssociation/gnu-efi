%define debug_package %{nil}
%define dirver	%(echo %{version}|sed -e 's/[a-z]//g')

Summary:	Development Libraries and headers for EFI
Name:		gnu-efi
Version:	3.0v
Release:	3
Group:		System/Kernel and hardware
License:	BSD
Url:		http://sourceforge.net/projects/gnu-efi
Source0:	http://freefr.dl.sourceforge.net/project/gnu-efi/gnu-efi_%{version}.orig.tar.gz
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
# Makefiles aren't SMP clean
make PREFIX=%{_prefix} LIBDIR=%{_libdir} LD=ld.bfd INSTALLROOT=%{buildroot}
make -C apps t.efi t2.efi t3.efi t4.efi t5.efi t6.efi printenv.efi t7.efi tcc.efi modelist.efi route80h.efi drv0_use.efi AllocPages.efi FreePages.efi PREFIX=%{_prefix} LIBDIR=%{_libdir} LD=ld.bfd INSTALLROOT=%{buildroot}

%install
# Unfortunately as of 3.0v, the make install target is completely broken.
# (3.0u is ok)
# FIXME revert to using make install as the issue is fixed upstream.
# make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} install
mkdir -p %{buildroot}%{_libdir}/gnuefi
cp -a gnuefi/crt0-efi*.o gnuefi/*.lds %{buildroot}%{_libdir}/gnuefi/
cp -a */lib*.a %{buildroot}%{_libdir}/
mkdir -p %{buildroot}/boot/efi/EFI/omdv
cp -a apps/*.efi %{buildroot}/boot/efi/EFI/omdv/
mkdir -p %{buildroot}%{_includedir}
rm -f inc/Makefile inc/inc.mak inc/makefile.hdr inc/make.inf
cp -a inc %{buildroot}%{_includedir}/efi

%files
%doc README.* ChangeLog
%{_includedir}/efi
%{_libdir}/gnuefi
%{_libdir}/*.a
%dir /boot/efi/EFI/omdv/
%attr(0644,root,root) /boot/efi/EFI/omdv/*.efi

