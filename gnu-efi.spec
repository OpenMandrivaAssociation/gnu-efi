# Work around incomplete debug packages
%undefine _debugsource_packages

%global __strip %{__strip} -gDp

%global __requires_exclude pkg-config

%define _disable_lto 1
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
Version:	3.0.18
Release:	1
Group:		System/Kernel and hardware
License:	BSD
Url:		http://sourceforge.net/projects/gnu-efi
Source0:	http://freefr.dl.sourceforge.net/project/gnu-efi/gnu-efi-%{version}.tar.bz2
Source100:	%{name}.rpmlintrc
Patch0:		gnu-efi-3.0.10-fallthroug.patch
#Patch1:		https://sourceforge.net/p/gnu-efi/patches/70/attachment/gnu-efi-3.0.9-fix-clang-build.patch
# The sbat patch is BROKEN (incomptaible with PIC code).
# Don't reactivate it unless you've fixed it up to not break fwupdate build first.
#Patch2:	gnu-efi-bsc1182057-support-sbat-section.patch
Patch3:		gnu-efi-3.0.14-add-pkgconfig-support.patch
# (tpg) force no executable stack
Patch4:		gnu-efi-3.0.15-no-executable-stack.patch
BuildRequires:	kernel-source
BuildRequires:	efi-srpm-macros
# (tpg) this is needed for ld.bfd
BuildRequires:	binutils
BuildRequires:	findutils
ExclusiveArch:	%{efi}

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%autosetup -n %{name}-%{dirver} -p1

%build
# Makefiles aren't SMP clean and do not pass
# our optflags and ldflags as this does not link to any C library
# (tpg) ld.lld does not uderstand custom linker script (elf_*_efi.lds), so let's hardcode to ld.bfd
make CC=%{__cc} HOSTCC=%{__cc} LD="ld.bfd"
make CC=%{__cc} HOSTCC=%{__cc} LD="ld.bfd" apps

%install
mkdir -p %{buildroot}%{_libdir}
make CC=%{__cc} HOSTCC=%{__cc} LD="ld.bfd" PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} install

mkdir -p %{buildroot}%{_libdir}/gnuefi
mv %{buildroot}%{_libdir}/*.lds %{buildroot}%{_libdir}/*.o %{buildroot}%{_libdir}/gnuefi
for i in $(find %{buildroot}%{_libdir} -type f -name "*.a" -printf "%f\n"); do
    ln -sf %{_libdir}/$i %{buildroot}%{_libdir}/gnuefi/$i
done

# (tpg) do not install efi images on /boot
mkdir -p %{buildroot}%{_libdir}/gnuefi/apps
cp -a %{efiarch}/apps/*.efi %{buildroot}/%{_libdir}/gnuefi/apps

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

%files
%doc README.* ChangeLog
%{_includedir}/efi
%{_libdir}/gnuefi
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
