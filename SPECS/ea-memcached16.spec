%global ns_dir /opt/cpanel

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

%if 0%{?centos} >= 7 || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

Name:    ea-memcached16
Vendor:  cPanel, Inc.
Summary: Memcached
Version: 1.6.39
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: Memcached
Group:   System Environment/Daemons
URL: https://github.com/memcached/memcached/wiki

Source0: %{version}.tar.gz
Source1: README.md
Source2: pkg.prerm

# if I do not have autoreq=0, rpm build will recognize that the ea_
# scripts need perl and some Cpanel pm's to be on the disk.
# unfortunately they cannot be satisfied via the requires: tags.
Autoreq: 0

Requires: ea-podman

%description
Memcached is an in-memory key-value store for small arbitrary data (strings,
objects) from results of database calls, API calls, or page rendering.

%prep

# nothing to do here

%build
# empty build section

%install

mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16
cp %{SOURCE1} $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16/README.md
echo -n "%{version}-%{release_prefix}" > $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16/pkg-version

cat << EOF > $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16/ea-podman.json
{
    "ports" : [],
    "image" : "docker.io/library/memcached:%{version}",
    "startup" : {
        "--user" : [ "root" ],
        "-v"     : [ ":/socket_dir" ],
        "--entrypoint" : [ "[\"/entrypoint.sh\",\"-u\",\"root\",\"-s\",\"/socket_dir/memcached.sock\"]" ]
    }
}
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%preun

%include %{SOURCE2}

%files
%defattr(0644,root,root,-)
/opt/cpanel/ea-memcached16

%changelog
* Tue Jul 29 2025 Cory McIntire <cory.mcintire@webpros.com> - 1.6.39-1
- EA-13047: Update ea-memcached16 from v1.6.38 to v1.6.39

* Thu Mar 20 2025 Cory McIntire <cory.mcintire@webpros.com> - 1.6.38-1
- EA-12781: Update ea-memcached16 from v1.6.37 to v1.6.38

* Sat Feb 22 2025 Cory McIntire <cory.mcintire@webpros.com> - 1.6.37-1
- EA-12728: Update ea-memcached16 from v1.6.36 to v1.6.37

* Wed Feb 05 2025 Cory McIntire <cory.mcintire@webpros.com> - 1.6.36-1
- EA-12685: Update ea-memcached16 from v1.6.34 to v1.6.36

* Tue Dec 24 2024 Cory McIntire <cory@cpanel.net> - 1.6.34-1
- EA-12620: Update ea-memcached16 from v1.6.33 to v1.6.34

* Fri Dec 06 2024 Cory McIntire <cory@cpanel.net> - 1.6.33-1
- EA-12600: Update ea-memcached16 from v1.6.14 to v1.6.33

* Mon May 08 2023 Julian Brown <julian.brown@cpanel.net> - 1.6.14-2
- ZC-10936: Clean up Makefile and remove debug-package-nil

* Wed Mar 04 2022 Julian Brown <julian.brown@cpanel.net> - 1.6.14-1
- ZC-8430: Add container based memcached

