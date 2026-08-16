#!/usr/bin/env bash
set -euo pipefail

IP=$1
ENDPOINT=${2:-kube-api.local}

## sudo kubeadm reset
if grep -qE "[[:space:]]${ENDPOINT}$" /etc/hosts; then
  sed -i -E "s#^.*[[:space:]]${ENDPOINT}$#${IP} ${ENDPOINT}#" /etc/hosts
else
  echo "${IP} ${ENDPOINT}" >> /etc/hosts
fi

systemctl restart containerd
kubeadm init \
  --control-plane-endpoint "${ENDPOINT}" \
  --apiserver-advertise-address "${IP}" \
  --token-ttl 8760h >> /tmp/run_kube_init.sh
