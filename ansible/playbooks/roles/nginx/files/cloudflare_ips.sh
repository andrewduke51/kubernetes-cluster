#!/usr/bin/bash

set -e

cf_ips() {
echo "# https://www.cloudflare.com/ips"

for type in v4 v6; do
echo "# IP$type"
curl -sL "https://www.cloudflare.com/ips-$type/" | sed "s|^|allow |g" | sed "s|\$|;|g"
echo
done

echo "#CF Update Generated at $(LC_ALL=C date)" > /tmp/cf.log
}
(cf_ips && echo "#deny all; # deny all remaining ips") > /etc/nginx/allow-cloudflare-only.conf