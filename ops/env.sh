#!/bin/bash
set -euo pipefail

: "${CONFIG:?CONFIG must contain the base64 encoded kubeconfig}"
: "${LOCAL_VARS:?LOCAL_VARS must contain the base64 encoded Ansible vars}"
: "${INVENTORY:?INVENTORY must contain the base64 encoded Ansible inventory}"
: "${CIRCLE_WORKING_DIRECTORY:?CIRCLE_WORKING_DIRECTORY must be set}"

mkdir -p local_files

printf '%s' "${CONFIG}"     | base64 -d > "${CIRCLE_WORKING_DIRECTORY}/ops/config"
chmod go-r "${CIRCLE_WORKING_DIRECTORY}/ops/config"

printf '%s' "${LOCAL_VARS}" | base64 -d > "local_files/ansible_local_vars.yml"
printf '%s' "${INVENTORY}"  | base64 -d > "local_files/inventory"

# make it available immediately + for later steps
export KUBECONFIG="${CIRCLE_WORKING_DIRECTORY}/ops/config"
echo "export KUBECONFIG=${CIRCLE_WORKING_DIRECTORY}/ops/config" >> "${BASH_ENV}"

api_server="$(kubectl --kubeconfig "${KUBECONFIG}" config view --minify -o jsonpath='{.clusters[0].cluster.server}')"
expected_api_server="${EXPECTED_KUBE_API_SERVER:-https://kube-api.local:6443}"

if [ "${api_server}" != "${expected_api_server}" ]; then
  echo "Unexpected Kubernetes API server in CONFIG: ${api_server}" >&2
  echo "Expected: ${expected_api_server}" >&2
  exit 1
fi

for host in k-master k-worker-01 k-worker-02; do
  if ! awk -v host="${host}" '$1 == host { found = 1 } END { exit found ? 0 : 1 }' local_files/inventory; then
    echo "Decoded INVENTORY is missing expected host: ${host}" >&2
    exit 1
  fi
done

echo "Using Kubernetes API server: ${api_server}"
awk '/^(k-master|k-worker-01|k-worker-02)[[:space:]]/ { print "Inventory host:", $1 }' local_files/inventory
