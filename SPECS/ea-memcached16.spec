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

%if 0%{?rhel} >= 8
%global debug_package %{nil}
%endif

Name:    ea-memcached16
Vendor:  cPanel, Inc.
Summary: Memcached
Version: 1.6.14
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: Memcached
Group:   System Environment/Daemons
URL: https://github.com/memcached/memcached/wiki

Source1: ea-podman-local-dir-setup
Source2: README.md

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
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16
cp %{SOURCE1} $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16/ea-podman-local-dir-setup
cp %{SOURCE2} $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16/README.md
echo -n "%{version}-%{release_prefix}" > $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16/pkg-version

cp %{SOURCE1} $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16/ea-podman-local-dir-setup
cp %{SOURCE2} $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16/README.md

cat << EOF > $RPM_BUILD_ROOT/opt/cpanel/ea-memcached16/ea-podman.json
{
    "image" : "docker.io/library/memcached:%{version}",
    "startup" : {
        "-v" : [ "socket_dir:/socket_dir" ],
        "--entrypoint" : [ "[\"/entrypoint.sh\", \"-s\", \"/socket_dir/memcached.sock\"]" ]
    }
}
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/cpanel/ea-memcached16
%attr(0655,root,root) /opt/cpanel/ea-memcached16
%attr(0755,root,root) /opt/cpanel/ea-memcached16/ea-podman-local-dir-setup
%attr(0644,root,root) /opt/cpanel/ea-memcached16/ea-podman.json
%attr(0644,root,root) /opt/cpanel/ea-memcached16/README.md

%changelog
* Wed Mar 04 2022 Julian Brown <julian.brown@cpanel.net> - 1.6.14-1
- ZC-8430: Add container based memcached

