#!/bin/bash

HELM_VERSION=3.7.2

# install kubectl
cd ops && curl -LO https://dl.k8s.io/release/v1.25.0/bin/linux/amd64/kubectl
chmod +x kubectl

## Install helm ##
curl -LO "https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz" -o helm-v${HELM_VERSION}-linux-amd64.tar.gz
tar -zxvf "helm-v${HELM_VERSION}-linux-amd64.tar.gz"
mv linux-amd64/helm helm
chmod +x helm

# set config
mkdir ../local_files
echo "${CONFIG}" | base64 -d > config
chmod go-r config

# set ansible_local_vars
echo "${LOCAL_VARS}" | base64 -d > ../local_files/ansible_local_vars.yml
echo "${INVENTORY}" | base64 -d > ../local_files/inventory
echo "export KUBECONFIG=${CIRCLE_WORKING_DIRECTORY}/ops/config" >> ${BASH_ENV}