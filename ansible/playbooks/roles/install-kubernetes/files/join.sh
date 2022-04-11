#!/usr/bin/env bash

KUBE_TOKEN=$1
TOKEN_CERT_HASH=$2

FILE= /etc/containerd/done
if [[ -f "$FILE" ]]; then
  echo "file exists"
else
  rm /etc/containerd/config.toml
  systemctl enable containerd
  systemctl daemon-reload
  systemctl restart containerd
  kubeadm join kube-api.local:6443 --token ${KUBE_TOKEN} --discovery-token-ca-cert-hash ${TOKEN_CERT_HASH}
  touch /etc/containerd/done
fi