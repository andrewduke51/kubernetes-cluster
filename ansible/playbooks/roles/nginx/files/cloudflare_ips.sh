#!/usr/bin/bash

set -e

cf_ips() {
echo "# https://www.cloudflare.com/ips"
echo "allow 70.161.198.2/32;"
echo "allow 192.168.1.20/32;"
echo "allow 192.168.1.1/32;"
echo "allow 174.250.14.3/32;"

for type in v4 v6; do
echo "# IP$type"
curl -sL "https://www.cloudflare.com/ips-$type/" | sed "s|^|allow |g" | sed "s|\$|;|g"
echo
done

echo "# Generated at $(LC_ALL=C date)"
}
(cf_ips && echo "#deny all; # deny all remaining ips") > /etc/nginx/allow-cloudflare-only.conf