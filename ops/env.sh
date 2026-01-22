#!/bin/bash
set -euo pipefail

mkdir -p local_files

echo "${CONFIG}" | base64 -d > "local_files/config"
chmod go-r "local_files/config"

echo "${LOCAL_VARS}" | base64 -d > "local_files/ansible_local_vars.yml"
echo "${INVENTORY}"  | base64 -d > "local_files/inventory"

## make it available immediately + for later steps
#export KUBECONFIG="${CIRCLE_WORKING_DIRECTORY}/ops/config"
#echo "export KUBECONFIG=${CIRCLE_WORKING_DIRECTORY}/ops/config" >> "${BASH_ENV}"
