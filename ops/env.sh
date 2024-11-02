#!/bin/sh

# set config
pwd
mkdir ../local_files
echo "${CONFIG}" | base64 -d > ${CIRCLE_WORKING_DIRECTORY}/ops/config
chmod go-r ${CIRCLE_WORKING_DIRECTORY}/ops/config

## set ansible_local_vars
echo "${LOCAL_VARS}" | base64 -d > ../local_files/ansible_local_vars.yml
echo "${INVENTORY}" | base64 -d > ../local_files/inventory
echo "export KUBECONFIG=${CIRCLE_WORKING_DIRECTORY}/ops/config" >> ${BASH_ENV}