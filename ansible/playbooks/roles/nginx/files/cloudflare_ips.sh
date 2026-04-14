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

local_private_cidrs() {
  echo "# Local private networks"

  ip -o -4 route show proto kernel scope link 2>/dev/null \
    | awk '
      $1 ~ /^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)/ &&
      $0 !~ / dev (docker|br-|veth|cni|flannel|weave)/ {
        print "allow " $1 "; # local private network"
      }
    '

  if [ -n "${EXTRA_ALLOWED_CIDRS:-}" ]; then
    printf '%s\n' "${EXTRA_ALLOWED_CIDRS}" \
      | tr ',' '\n' \
      | awk 'NF { print "allow " $1 "; # extra allowed network" }'
  fi

  echo
}

(
  cf_ips
  local_private_cidrs
  echo "deny all; # deny all remaining ips"
) > /etc/nginx/allow-cloudflare-only.conf
