#!/usr/bin/bash
set -euo pipefail

cf_ips() {
  echo "# https://www.cloudflare.com/ips"

  for type in v4 v6; do
    echo "# IP$type"
    curl -sL "https://www.cloudflare.com/ips-$type/" | sed 's|^|allow |; s|$|;|'
    echo
  done

  echo "# CF Update Generated at $(LC_ALL=C date)"
}

(cf_ips && echo "deny all; # deny all remaining ips") > /etc/nginx/allow-cloudflare-only.conf