#!/bin/bash

source debian/vars.sh

mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-container-memcached
echo -n "$version-$release_prefix" > pkg-version
cp pkg-version $DEB_INSTALL_ROOT/opt/cpanel/ea-container-memcached/pkg-version
cp $SOURCE1 $DEB_INSTALL_ROOT/opt/cpanel/ea-container-memcached/ea-podman-local-dir-setup
cp $SOURCE2 $DEB_INSTALL_ROOT/opt/cpanel/ea-container-memcached/README.md
cp $SOURCE1 .
cp $SOURCE2 .
cat << EOF > ea-podman.json
{
    "image" : "docker.io/library/memcached:$version",
    "startup" : {
        "-v" : [ "socket_dir:/socket_dir" ],
        "--entrypoint" : [ "[\"/entrypoint.sh\", \"-s\", \"/socket_dir/memcached.sock\"]" ]
    }
}
EOF
cp ea-podman.json $DEB_INSTALL_ROOT/opt/cpanel/ea-container-memcached/ea-podman.json
