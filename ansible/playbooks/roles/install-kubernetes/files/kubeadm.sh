#!/usr/bin/env bash

IP=$1

## sudo kubeadm reset
echo "${IP} kube-api.local" >> /etc/hosts
systemctl restart containerd
kubeadm init --control-plane-endpoint localhost --control-plane-endpoint kube-api.local --apiserver-advertise-address ${IP} --token-ttl 8760h >> /tmp/run_kube_init.sh